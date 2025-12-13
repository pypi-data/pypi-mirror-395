import warnings

import pandas as pd
import time

from seeq import spy
from seeq.base import util
from seeq.sdk import *
from seeq.sdk.rest import ApiException
from seeq.spy import Session, _pull, _common
from seeq.spy.tests import test_common
from seeq.spy.workbooks import Room


def setup_module():
    test_common.initialize_sessions()


VANTAGE_ROOM_SINUSOID_CUTOFF_DATETIME = pd.to_datetime('2025-01-01T06:00:00Z')


def _ensure_vantage_label_categories_and_labels(session: Session, test_label_category_name: str, test_label_name: str):
    return util.os_lock(
        'vantage_test_labels',
        _ensure_vantage_label_categories_and_labels_internal,
        args=(session, test_label_category_name, test_label_name),
        timeout=60
    )


def _ensure_vantage_label_categories_and_labels_internal(session: Session, test_label_category_name: str, test_label_name: str):
    context_api = ContextApi(session.client)

    label_categories_output = context_api.find_label_categories()
    label_categories = {lc.name: lc.id for lc in label_categories_output.categories}

    if test_label_category_name not in label_categories:
        try:
            label_categories[test_label_category_name] = context_api.create_label_category(
                body=LabelCategoryInputV1(name=test_label_category_name)
            ).id
        except ApiException as e:
            if 'already exists' not in _common.format_exception(e):
                raise
            # If it was created by another process between check and create, fetch it again
            label_categories_output = context_api.find_label_categories()
            label_categories = {lc.name: lc.id for lc in label_categories_output.categories}

    def _refresh_labels():
        refreshed = dict()
        for _, label_category_id in label_categories.items():
            label_output_list = context_api.find_labels(category_id=label_category_id)
            refreshed.update({lc.name: lc.id for lc in label_output_list.labels})
        return refreshed

    def _ensure_label(label_name, category_id):
        if label_name in labels:
            return labels[label_name]

        try:
            label_id = context_api.create_label(
                body=LabelInputV1(
                    category_id=category_id,
                    name=label_name
                )
            ).id
            labels[label_name] = label_id
            return label_id
        except ApiException as e:
            if 'already exists' not in _common.format_exception(e):
                raise
            # Label was created by another process, refresh and return
            labels.update(_refresh_labels())
            return labels[label_name]

    labels = _refresh_labels()

    # Create the built-in labels that the front-end would normally create on first use
    vantage_labels_category_id = label_categories['__Vantage.labels']
    for built_in_label in ['Model Maintenance', 'Documented', 'Validating', 'flag']:
        _ensure_label(built_in_label, vantage_labels_category_id)

    # Create the test label
    _ensure_label(test_label_name, label_categories[test_label_category_name])

    return labels


def create_vantage_room(session: Session):
    test_id = _common.new_placeholder_guid()

    my_vantage_room = Room({'Name': f'My Vantage Room {test_id}'})
    my_vantage_room_view = my_vantage_room.view('My View')
    my_vantage_room_view.investigate_range = {'Start': '2024-02-12', 'End': '2024-12-14T00:00:00.001+00:00'}

    spy.workbooks.push(my_vantage_room, session=session)

    table_definition_id = my_vantage_room['Evidence Table Definition ID']

    seconds_since_cutoff_date = int(
        (pd.Timestamp.now(tz='UTC') - VANTAGE_ROOM_SINUSOID_CUTOFF_DATETIME).total_seconds())
    my_vantage_condition_df = spy.push(metadata=pd.DataFrame([{
        'Type': 'Condition',
        'Name': f'My Vantage Condition {test_id}',
        'Formula': f'sinusoid(1d).remove(past().move(-{seconds_since_cutoff_date}s).inverse()) > 0',
    }]), session=session)

    my_vantage_condition_list = my_vantage_condition_df['ID'].to_list()
    my_vantage_condition_id = my_vantage_condition_list[0]

    condition_monitors_api = ConditionMonitorsApi(session.client)
    condition_monitor = condition_monitors_api.create_condition_monitor(body=ConditionMonitorInputV1(
        name=f'My Vantage Condition Monitor {test_id}',
        condition_ids=my_vantage_condition_list,
        first_run_look_back=seconds_since_cutoff_date + 31 * 24 * 60 * 60 + 7 * 60 * 60,  # 31 days before cutoff
        scoped_to=my_vantage_room.id,
        capsule_event_types=["NEW", "BECAME_CERTAIN", "EXTINCT", "STILL_UNCERTAIN"]
    ))

    table_definitions_api = TableDefinitionsApi(session.client)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        table_definition = table_definitions_api.update_table_definition(
            id=table_definition_id,
            body=TableDefinitionUpdateInputV1(
                name=f'My Vantage Table {test_id}',
                subscription_id=condition_monitor.id,
                batch_action='UPDATE_EXISTING_INSERT_NEW_CLEANUP'
            ))

    end = VANTAGE_ROOM_SINUSOID_CUTOFF_DATETIME + pd.Timedelta(days=1)
    start = end - pd.Timedelta(days=60)

    while True:
        graphql_output = _pull.graphql_get_evidence(
            session,
            table_definition.id,
            start,
            end,
            None,
            1_000,
            True
        )

        if len(graphql_output['data']['table']['rows']) >= 32:
            break

        time.sleep(0.1)

    # Use os_lock to ensure only one test process creates label categories and labels at a time
    # This prevents race conditions when multiple tests run in parallel
    my_label_category = f'My Vantage Label Category {test_id}'
    my_label_1 = 'My Label #1'
    labels = _ensure_vantage_label_categories_and_labels(session, my_label_category, my_label_1)
    headers = {v['name']: i for i, v in enumerate(graphql_output['data']['table']['headers'])}

    second_capsule = graphql_output['data']['table']['rows'][1]
    second_capsule_start = pd.Timestamp(second_capsule[headers['Start']])
    second_capsule_end = pd.Timestamp(second_capsule[headers['End']])

    context_api = ContextApi(session.client)
    context_api.create_context_comment(
        item_id=my_vantage_condition_id,
        body=ContextCommentInputV1(
            datum_id=second_capsule[headers['datum id']],
            comment="This is comment #1",
            start_time=(second_capsule_start + pd.Timedelta(hours=1)).isoformat() + 'Z',
            end_time=(second_capsule_start + pd.Timedelta(hours=3)).isoformat() + 'Z'
        )
    )

    context_api.create_context_comment(
        item_id=my_vantage_condition_id,
        body=ContextCommentInputV1(
            datum_id=second_capsule[headers['datum id']],
            comment="This is comment #2",
            start_time=(second_capsule_start + pd.Timedelta(hours=3)).isoformat() + 'Z',
            end_time=(second_capsule_end).isoformat() + 'Z'
        )
    )

    context_labels = dict()
    context_labels[my_label_1] = context_api.create_context_label(
        item_id=my_vantage_condition_id,
        body=ContextLabelInputV1(
            datum_id=second_capsule[headers['datum id']],
            label_id=labels[my_label_1],
            start_time=(second_capsule_start + pd.Timedelta(hours=2)).isoformat() + 'Z',
            end_time=(second_capsule_start + pd.Timedelta(hours=3)).isoformat() + 'Z'
        )
    ).archiver_id

    context_labels['Documented'] = context_api.create_context_label(
        item_id=my_vantage_condition_id,
        body=ContextLabelInputV1(
            datum_id=second_capsule[headers['datum id']],
            label_id=labels['Documented'],
            start_time=(second_capsule_start + pd.Timedelta(hours=4)).isoformat() + 'Z',
            end_time=(second_capsule_end - pd.Timedelta(hours=1)).isoformat() + 'Z'
        )
    ).archiver_id

    boolean_label_name = 'flag'
    context_labels[boolean_label_name] = context_api.create_context_label(
        item_id=my_vantage_condition_id,
        body=ContextLabelInputV1(
            datum_id=second_capsule[headers['datum id']],
            label_id=labels[boolean_label_name],
            start_time=second_capsule_start.isoformat() + 'Z',
            end_time=second_capsule_end.isoformat() + 'Z'
        )
    ).archiver_id

    numeric_description_output_list: NumericDescriptionOutputListV1 = context_api.get_all_numeric_descriptions()
    numeric_descriptions = {nd.name: nd.id for nd in numeric_description_output_list.numeric_descriptions}
    my_numeric_description = f'My Vantage Numeric Description {test_id}'
    if my_numeric_description not in numeric_descriptions:
        numeric_descriptions[my_numeric_description] = context_api.create_numeric_description(
            body=NumericDescriptionInputV1(
                name=my_numeric_description,
                max=100.0,
                min=-100.0,
                precision=0.1,
                unit_of_measure='m'
            )
        ).id

    try:
        context_api.create_context_numeric(
            item_id=my_vantage_condition_id,
            body=ContextNumericInputV1(
                datum_id=second_capsule[headers['datum id']],
                numeric_description_id=numeric_descriptions[my_numeric_description],
                start_time=(second_capsule_start + pd.Timedelta(hours=1)).isoformat() + 'Z',
                end_time=(second_capsule_end).isoformat() + 'Z',
                value=42.0
            )
        )
    except ApiException as e:
        if 'already exists' not in _common.format_exception(e):
            raise

    return my_vantage_room
