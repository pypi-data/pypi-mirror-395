from datetime import date, time, timedelta
import json

import math
import pandas as pd
import pytest

import httpretty

from pandas.testing import assert_frame_equal

from swiftly_api_client import (
    SwiftlyAPIClient,
    SwiftlyAPIClientError,
    SwiftlyAPIServerError,
)
from swiftly_api_client.network import configure_requests_session


@httpretty.activate
def test_handle_client_error():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {"errorCode": 403, "errorMessage": "Permission Denied"}

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=403,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key="test_agency", api_key="test_api_key")

    with pytest.raises(SwiftlyAPIClientError):
        client.get_runtimes_for_route_by_trip(
            route_short_name="test_route", start_date=target_date
        )


@httpretty.activate
def test_handle_server_error():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {"errorCode": 500, "errorMessage": "Server Error"}

    session = configure_requests_session(retries=2, backoff_factor=0.0)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
        ],
    )

    client = SwiftlyAPIClient(
        agency_key="test_agency", api_key="test_api_key", session=session
    )

    with pytest.raises(SwiftlyAPIServerError):
        client.get_runtimes_for_route_by_trip(
            route_short_name="test_route", start_date=target_date
        )


@httpretty.activate
def test_get_runtimes_for_route_by_trip():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {
        "route": path,
        "success": True,
        "result": {
            "direction-0": [
                {
                    "tripId": "test_trip_id",
                    "runtime": 12345,
                    "scheduledRuntime": 12345,
                    "scheduledDepartureSeconds": 600,
                    "timeFromStartUntilNextTrip": 54321,
                    "tripPattern": "gherogherog",
                    "firstStop": "test_first_stop",
                    "lastStop": "test_last_stop",
                    "observedRuntimes": [
                        {
                            "date": target_date.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        }
                    ],
                }
            ],
            "direction-1": [],
        },
    }

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=200,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key="test_agency", api_key="test_api_key")

    runtimes_resp = client.get_runtimes_for_route_by_trip(
        route_short_name="test_route", start_date=target_date
    )

    assert runtimes_resp == expected_response["result"]

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == [target_date.strftime("%m-%d-%Y")]


@httpretty.activate
def test_get_runtimes_for_route_by_trip_with_multiple_dates():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()
    target_date_2 = date.today() - timedelta(days=1)

    expected_response = {
        "route": path,
        "success": True,
        "result": {
            "direction-0": [
                {
                    "tripId": "test_trip_id",
                    "runtime": 12345,
                    "scheduledRuntime": 12345,
                    "scheduledDepartureSeconds": 600,
                    "timeFromStartUntilNextTrip": 54321,
                    "tripPattern": "gherogherog",
                    "firstStop": "test_first_stop",
                    "lastStop": "test_last_stop",
                    "observedRuntimes": [
                        {
                            "date": target_date_2.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        },
                        {
                            "date": target_date.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        },
                    ],
                }
            ],
            "direction-1": [],
        },
    }

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=200,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    runtimes_resp = client.get_runtimes_for_route_by_trip(
        route_short_name="test_route", start_date=target_date
    )

    assert runtimes_resp == expected_response["result"]


@httpretty.activate
def test_get_on_time_performance_export():
    agency = "test_agency"
    target_date = date(2020, 12, 21)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/otp/{agency}/csv-export"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open("tests/fixtures/nctd_swiftly_otp_export_2020-12-21.csv", "r") as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_on_time_performance_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 5],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
            use_service_dates=False,
            only_first_stop_of_trip=True,
        )
        assert (
            df[df["trip_id"] == "15141675-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30102
        )
        assert (
            df[df["trip_id"] == "15141699-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30106
        )
        assert (
            df[df["trip_id"] == "15141691-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30104
        )

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["12-21-2020"]
    assert sent_req.querystring["endDate"] == ["12-21-2020"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,5"]
    assert sent_req.querystring["excludeDates"] == ["12-22-2020,12-23-2020"]
    assert sent_req.querystring["useServiceDates"] == ["false"]
    assert sent_req.querystring["onlyFirstStopOfTrip"] == ["true"]

    df = client.get_on_time_performance_export(
        start_date=target_date,
        end_date=target_date,
        route="NC2010",
    )
    assert (
        df[df["trip_id"] == "15141675-NC2010-NCTD-Weekday-06"].iloc[0].block_id == 30102
    )
    assert (
        df[df["trip_id"] == "15141699-NC2010-NCTD-Weekday-06"].iloc[0].block_id == 30106
    )
    assert (
        df[df["trip_id"] == "15141691-NC2010-NCTD-Weekday-06"].iloc[0].block_id == 30104
    )

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["12-21-2020"]
    assert sent_req.querystring["endDate"] == ["12-21-2020"]
    assert sent_req.querystring["route"] == ["NC2010"]


@httpretty.activate
def test_get_trip_observations_export_single_vehicles():
    agency = "test_agency"
    target_date = date(2023, 6, 30)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/run-times/{agency}/trip-observations"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""blockId,tripId,tripShortName,routeShortName,routeId,directionId,serviceId,tripPatternId,scheduledTripStartTime,serviceDate,observedTripStartTime,observedTripEndTime,secondsToNextTripInBlockScheduledStartTime,scheduledRuntimeSeconds,numScheduledStopsOnTrip,numStopsWithArrivalDepartureData,isCompleteTrip,totalStopPathLength,observedDwellSeconds,observedTravelSeconds,observedRuntimeSeconds,driverIds,vehicleIds,scheduleRelationship,adjustmentIds,adjustmentTypes
503-1,t_5561882_b_80157_tn_1,t_5561882_b_80157_tn_1,503,503,1,c_69241_b_80157_d_31,route_503_2561389_to_2561195_9e652c333c004f1edb920350d153a6f53514f9e293ed5cb3a473a51241a1f50d,05:30:00,2023-06-30,05:33:40,06:24:32,5400,3720,62,62,true,31085.13250732422,488.4921875,2563.963,3052.455,,2202,ADDED,,
403-1,t_5561912_b_80157_tn_0,t_5561912_b_80157_tn_0,403,403,1,c_69241_b_80157_d_31,route_403_2561121_to_2561195_d9b545300a47a081ac76b4d278e8b2d085775ee0bd9a8f4529c0694b55e1dde3,05:37:00,2023-06-30,,05:55:59,1380,780,13,8,false,5809.577941894531,,,,,2203,SCHEDULED,,
                """,
                status=200,
            ),
        ],
    )
    df = client.get_trip_observations_export(start_date=target_date)

    expected_df = pd.DataFrame(
        {
            "blockId": ["503-1", "403-1"],
            "tripId": ["t_5561882_b_80157_tn_1", "t_5561912_b_80157_tn_0"],
            "tripShortName": ["t_5561882_b_80157_tn_1", "t_5561912_b_80157_tn_0"],
            "routeShortName": ["503", "403"],
            "routeId": ["503", "403"],
            "directionId": ["1", "1"],
            "serviceId": ["c_69241_b_80157_d_31", "c_69241_b_80157_d_31"],
            "tripPatternId": [
                "route_503_2561389_to_2561195_9e652c333c004f1edb920350d153a6f53514f9e293ed5cb3a473a51241a1f50d",
                "route_403_2561121_to_2561195_d9b545300a47a081ac76b4d278e8b2d085775ee0bd9a8f4529c0694b55e1dde3",
            ],
            "scheduledTripStartTime": ["05:30:00", "05:37:00"],
            "serviceDate": ["2023-06-30", "2023-06-30"],
            "observedTripStartTime": ["05:33:40", math.nan],
            "observedTripEndTime": ["06:24:32", "05:55:59"],
            "secondsToNextTripInBlockScheduledStartTime": [5400, 1380],
            "scheduledRuntimeSeconds": [3720, 780],
            "numScheduledStopsOnTrip": [62, 13],
            "numStopsWithArrivalDepartureData": [62, 8],
            "isCompleteTrip": [True, False],
            "totalStopPathLength": [31085.13250732422, 5809.577941894531],
            "observedDwellSeconds": [488.4921875, math.nan],
            "observedTravelSeconds": [2563.963, math.nan],
            "observedRuntimeSeconds": [3052.455, math.nan],
            "driverIds": [math.nan, math.nan],
            "vehicleIds": ["2202", "2203"],
            "scheduleRelationship": ["ADDED", "SCHEDULED"],
            "adjustmentIds": [math.nan, math.nan],
            "adjustmentTypes": [math.nan, math.nan],
        }
    )
    assert_frame_equal(df, expected_df)


@httpretty.activate
def test_get_trip_observations_export():
    agency = "test_agency"
    target_date = date(2023, 6, 30)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/run-times/{agency}/trip-observations"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open(
        "tests/fixtures/rtacm_swiftly_trip_observations_export_2023-06-30.csv", "r"
    ) as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_trip_observations_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 6, 7],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
            routes=["5561911", "5561915"],
        )
        assert (
            df[df["tripId"] == "t_5561911_b_80157_tn_0"].iloc[0].scheduleRelationship
            == "SCHEDULED"
        )
        assert (
            df[df["tripId"] == "t_5561915_b_80157_tn_11"].iloc[0].scheduleRelationship
            == "CANCELED"
        )

        assert math.isnan(
            df[df["tripId"] == "t_5561911_b_80157_tn_0"].iloc[0].vehicleIds
        )
        assert df[df["tripId"] == "t_5561882_b_80157_tn_1"].iloc[0].vehicleIds == "2202"
        assert (
            df[df["tripId"] == "t_5561916_b_80157_tn_0"].iloc[0].vehicleIds
            == "2201,2205"
        )
        assert df[df["tripId"] == "t_5561912_b_80157_tn_0"].iloc[0].vehicleIds == "2203"

        assert math.isnan(
            df[df["tripId"] == "t_5561823_b_80157_tn_0"].iloc[0].vehicleIds
        )
        assert math.isnan(
            df[df["tripId"] == "t_5561915_b_80157_tn_11"].iloc[0].vehicleIds
        )

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["06-30-2023"]
    assert sent_req.querystring["endDate"] == ["06-30-2023"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,6,7"]
    assert sent_req.querystring["excludeDates"] == ["07-01-2023,07-02-2023"]
    assert sent_req.querystring["routes"] == ["5561911,5561915"]


@httpretty.activate
def test_get_trip_observations_export_empty():
    agency = "test_agency"
    target_date = date(2023, 6, 30)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/run-times/{agency}/trip-observations"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open(
        "tests/fixtures/rtacm_swiftly_trip_observations_export_empty.csv", "r"
    ) as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_trip_observations_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 6, 7],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
        )
        assert df.empty

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["06-30-2023"]
    assert sent_req.querystring["endDate"] == ["06-30-2023"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,6,7"]
    assert sent_req.querystring["excludeDates"] == ["07-01-2023,07-02-2023"]


@httpretty.activate
def test_get_raw_apc_events():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/ridership/{agency}/apc-raw-events"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""
                {
                    "apcRawEvents": [
                        {
                            "id": 21293621,
                            "vehicle_id": "2203",
                            "time": "2023-10-01 08:16:56.997",
                            "latitude": 39.128956,
                            "longitude": -76.803697,
                            "ons": 0,
                            "offs": 0
                        },
                        {
                            "id": 21293622,
                            "vehicle_id": "2203",
                            "time": "2023-10-01 08:16:57.006",
                            "latitude": 39.128956,
                            "longitude": -76.803697,
                            "ons": 0,
                            "offs": 0
                        }
                    ]
                }
                """,
                status=200,
            ),
        ],
    )
    data = client.get_raw_apc_events(target_date)

    assert data == [
        {
            "id": 21293621,
            "vehicle_id": "2203",
            "time": "2023-10-01 08:16:56.997",
            "latitude": 39.128956,
            "longitude": -76.803697,
            "ons": 0,
            "offs": 0,
        },
        {
            "id": 21293622,
            "vehicle_id": "2203",
            "time": "2023-10-01 08:16:57.006",
            "latitude": 39.128956,
            "longitude": -76.803697,
            "ons": 0,
            "offs": 0,
        },
    ]

    sent_req = httpretty.last_request()
    assert sent_req.querystring["date"] == ["2023-10-01"]


@httpretty.activate
def test_get_arrivals_departures_observations():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    url = client._format_url(client.ARRIVAL_DEPARTURE_OBSERVATIONS)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""block_id,trip_id,route_id,route_short_name,direction_id,stop_id,stop_name,stop_code,trip_headsign,departure_vehicle_id,arrival_vehicle_id,stop_order,gtfs_stop_sequence,trip_start_time,is_last_stop_of_trip,is_first_stop_of_trip,adjustment_ids,adjustment_types,adjustment_effects,schedule_adherence_secs,scheduled_arrival_time,scheduled_departure_time,observed_arrival_time,observed_departure_time,is_schedule_adherence_stop,service_date
401-1,t_5940767_b_83572_tn_6,401,401,0,2561195,Mall in Columbia,40000,Clary's Forest,,,0,1,14:00:00,false,true,,,,,14:00:00,14:00:00,,,true,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561170,Howard County Hospital East (Southbound),43019,Mall in Columbia,,,7,8,18:20:00,false,false,,,,,18:25:43,18:25:43,,,false,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561169,Howard County Hospital South (Southbound),43020,Mall in Columbia,,,8,9,18:20:00,false,false,,,,,18:26:00,18:26:00,,,false,2024-12-01
402-1,t_5940784_b_83572_tn_1,402,402,0,2561156,Knoll Dr / Columbia Medical Plan,40669,Dobbin Center via Long Reach,,,5,6,09:30:00,false,false,,,,,09:38:00,09:38:00,,,true,2024-12-01
402-1,t_5940784_b_83572_tn_2,402,402,0,2561156,Knoll Dr / Columbia Medical Plan,40669,Dobbin Center via Long Reach,,,5,6,10:30:00,false,false,,,,,10:38:00,10:38:00,,,true,2024-12-01
402-1,t_5940784_b_83572_tn_3,402,402,0,2561156,Knoll Dr / Columbia Medical Plan,40669,Dobbin Center via Long Reach,,,5,6,11:30:00,false,false,,,,,11:38:00,11:38:00,,,true,2024-12-01
                """,
                status=200,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date)

    expected_df = pd.DataFrame(
        {
            "block_id": ["401-1", "401-1", "401-1", "402-1", "402-1", "402-1"],
            "trip_id": [
                "t_5940767_b_83572_tn_6",
                "t_5940768_b_83572_tn_10",
                "t_5940768_b_83572_tn_10",
                "t_5940784_b_83572_tn_1",
                "t_5940784_b_83572_tn_2",
                "t_5940784_b_83572_tn_3",
            ],
            "route_id": ["401", "401", "401", "402", "402", "402"],
            "route_short_name": ["401", "401", "401", "402", "402", "402"],
            "direction_id": [0, 1, 1, 0, 0, 0],
            "scheduled_arrival_time": [
                "14:00:00",
                "18:25:43",
                "18:26:00",
                "09:38:00",
                "10:38:00",
                "11:38:00",
            ],
            "service_date": [
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
            ],
        }
    )

    # just compare some specific columns
    assert df[
        [
            "block_id",
            "trip_id",
            "route_id",
            "route_short_name",
            "direction_id",
            "scheduled_arrival_time",
            "service_date",
        ]
    ].equals(expected_df)

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["10-01-2023"]


@httpretty.activate
def test_get_arrivals_departures_observations_by_route():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    url = client._format_url(client.ARRIVAL_DEPARTURE_OBSERVATIONS)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""block_id,trip_id,route_id,route_short_name,direction_id,stop_id,stop_name,stop_code,trip_headsign,departure_vehicle_id,arrival_vehicle_id,stop_order,gtfs_stop_sequence,trip_start_time,is_last_stop_of_trip,is_first_stop_of_trip,adjustment_ids,adjustment_types,adjustment_effects,schedule_adherence_secs,scheduled_arrival_time,scheduled_departure_time,observed_arrival_time,observed_departure_time,is_schedule_adherence_stop,service_date
401-1,t_5940767_b_83572_tn_6,401,401,0,2561195,Mall in Columbia,40000,Clary's Forest,,,0,1,14:00:00,false,true,,,,,14:00:00,14:00:00,,,true,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561170,Howard County Hospital East (Southbound),43019,Mall in Columbia,,,7,8,18:20:00,false,false,,,,,18:25:43,18:25:43,,,false,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561169,Howard County Hospital South (Southbound),43020,Mall in Columbia,,,8,9,18:20:00,false,false,,,,,18:26:00,18:26:00,,,false,2024-12-01
                """,
                status=200,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date, routes=["401", "404"])

    expected_df = pd.DataFrame(
        {
            "block_id": ["401-1", "401-1", "401-1"],
            "trip_id": [
                "t_5940767_b_83572_tn_6",
                "t_5940768_b_83572_tn_10",
                "t_5940768_b_83572_tn_10",
            ],
            "route_id": ["401", "401", "401"],
            "route_short_name": ["401", "401", "401"],
            "direction_id": [0, 1, 1],
            "scheduled_arrival_time": [
                "14:00:00",
                "18:25:43",
                "18:26:00",
            ],
            "service_date": [
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
            ],
        }
    )

    # just compare some specific columns
    assert df[
        [
            "block_id",
            "trip_id",
            "route_id",
            "route_short_name",
            "direction_id",
            "scheduled_arrival_time",
            "service_date",
        ]
    ].equals(expected_df)

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["10-01-2023"]
    assert sent_req.querystring["routes"] == ["401,404"]


@httpretty.activate
def test_get_arrivals_departures_observations_by_vehicle():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    url = client._format_url(client.ARRIVAL_DEPARTURE_OBSERVATIONS)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""block_id,trip_id,route_id,route_short_name,direction_id,stop_id,stop_name,stop_code,trip_headsign,departure_vehicle_id,arrival_vehicle_id,stop_order,gtfs_stop_sequence,trip_start_time,is_last_stop_of_trip,is_first_stop_of_trip,adjustment_ids,adjustment_types,adjustment_effects,schedule_adherence_secs,scheduled_arrival_time,scheduled_departure_time,observed_arrival_time,observed_departure_time,is_schedule_adherence_stop,service_date
401-1,t_5940767_b_83572_tn_6,401,401,0,2561195,Mall in Columbia,40000,Clary's Forest,123,123,0,1,14:00:00,false,true,,,,,14:00:00,14:00:00,,,true,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561170,Howard County Hospital East (Southbound),43019,Mall in Columbia,123,123,7,8,18:20:00,false,false,,,,,18:25:43,18:25:43,,,false,2024-12-01
401-1,t_5940768_b_83572_tn_10,401,401,1,2561169,Howard County Hospital South (Southbound),43020,Mall in Columbia,123,123,8,9,18:20:00,false,false,,,,,18:26:00,18:26:00,,,false,2024-12-01
                """,
                status=200,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date, vehicles=["123"])

    expected_df = pd.DataFrame(
        {
            "block_id": ["401-1", "401-1", "401-1"],
            "trip_id": [
                "t_5940767_b_83572_tn_6",
                "t_5940768_b_83572_tn_10",
                "t_5940768_b_83572_tn_10",
            ],
            "route_id": ["401", "401", "401"],
            "route_short_name": ["401", "401", "401"],
            "direction_id": [0, 1, 1],
            "scheduled_arrival_time": [
                "14:00:00",
                "18:25:43",
                "18:26:00",
            ],
            "service_date": [
                "2024-12-01",
                "2024-12-01",
                "2024-12-01",
            ],
            "departure_vehicle_id": ["123", "123", "123"],
        }
    )

    # just compare some specific columns
    assert df[
        [
            "block_id",
            "trip_id",
            "route_id",
            "route_short_name",
            "direction_id",
            "scheduled_arrival_time",
            "service_date",
            "departure_vehicle_id",
        ]
    ].equals(expected_df)

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["10-01-2023"]
    assert sent_req.querystring["vehicles"] == ["123"]


@httpretty.activate
def test_get_arrivals_departures_observations_invalid_date_range():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/otp/{agency}/arrivals-departures"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""
                {
                    "errorCode":404,
                    "errorMessage":"Data is not available for the requested date range from this endpoint.
                    Try using the By Schedule endpoint instead."
                }""",
                status=404,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date)

    assert df.empty


@httpretty.activate
def test_get_arrivals_departures_observations_leading_zeroes():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    url = client._format_url(client.ARRIVAL_DEPARTURE_OBSERVATIONS)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""\
block_id,trip_id,route_id,route_short_name,direction_id,stop_id,stop_name,stop_code,trip_headsign,departure_vehicle_id,arrival_vehicle_id,stop_order,gtfs_stop_sequence,trip_start_time,is_last_stop_of_trip,is_first_stop_of_trip,adjustment_ids,adjustment_types,adjustment_effects,schedule_adherence_secs,scheduled_arrival_time,scheduled_departure_time,observed_arrival_time,observed_departure_time,is_schedule_adherence_stop,service_date
01,01,01,01,0,01,Route with Leading Zero,1,Route with Leading Zero,01,01,0,1,14:00:00,false,true,,,,,14:00:00,14:00:00,,,true,2024-12-01
                """,
                status=200,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date)

    expected_df = pd.DataFrame(
        {
            "block_id": ["01"],
            "trip_id": ["01"],
            "route_id": ["01"],
            "route_short_name": ["01"],
            "direction_id": [0],
            "stop_id": ["01"],
            "stop_name": ["Route with Leading Zero"],
            "stop_code": [1],
            "trip_headsign": ["Route with Leading Zero"],
            "departure_vehicle_id": ["01"],
            "arrival_vehicle_id": ["01"],
            "stop_order": [0],
            "gtfs_stop_sequence": [1],
            "scheduled_arrival_time": ["14:00:00"],
            "service_date": ["2024-12-01"],
        }
    )

    # just compare some specific columns
    assert df[
        [
            "block_id",
            "trip_id",
            "route_id",
            "route_short_name",
            "direction_id",
            "stop_id",
            "stop_name",
            "stop_code",
            "trip_headsign",
            "departure_vehicle_id",
            "arrival_vehicle_id",
            "stop_order",
            "gtfs_stop_sequence",
            "scheduled_arrival_time",
            "service_date",
        ]
    ].equals(expected_df)

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["10-01-2023"]


@httpretty.activate
def test_get_gps_playback():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/gps-playback/{agency}"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""
                {
                  "success": true,
                  "route": "/gps-playback/test_agency GET",
                  "data": {
                    "agencyKey": "test_agency",
                    "data": [
                      {
                        "time": "2018-06-02 07:59:04.136",
                        "lat": 37.77556,
                        "lon": -122.41857,
                        "speed": 0,
                        "heading": 46,
                        "headsign": "Caltrain/Ball Park",
                        "tripId": "8078058",
                        "blockId": "9708",
                        "vehicleId": "1410",
                        "routeId": "13142",
                        "assignmentId": "9708",
                        "directionId": "1",
                        "serviceName": "1 - Weekdays",
                        "serviceId": "1",
                        "isWaitStop": false,
                        "isLayover": false,
                        "isDelayed": false,
                        "timeProcessed": "2018-06-02 07:59:10.59",
                        "tripShortName": "8078058",
                        "routeShortName": "N",
                        "schedAdhMsec": 4468229,
                        "schedAdh": "74.5 minutes (late)",
                        "headwayMsec": 1898655,
                        "scheduledHeadwayMsec": 300000,
                        "previousVehicleId": "1405",
                        "previousVehicleSchedAdhMsec": -31776
                      },                      
                      {
                        "time": "2018-06-02 08:19:11.456",
                        "lat": 37.77328,
                        "lon": -122.39783,
                        "speed": 0,
                        "heading": 218,
                        "vehicleId": "1410",
                        "assignmentId": "9708",
                        "timeProcessed": "2018-06-02 08:19:19.498"
                      }
                    ]
                  }
                }
                """,
                status=200,
            ),
        ],
    )

    data = client.get_gps_playback(target_date, time(7, 50), time(8, 20), "1410")

    assert data == [
        {
            "time": "2018-06-02 07:59:04.136",
            "lat": 37.77556,
            "lon": -122.41857,
            "speed": 0,
            "heading": 46,
            "headsign": "Caltrain/Ball Park",
            "tripId": "8078058",
            "blockId": "9708",
            "vehicleId": "1410",
            "routeId": "13142",
            "assignmentId": "9708",
            "directionId": "1",
            "serviceName": "1 - Weekdays",
            "serviceId": "1",
            "isWaitStop": False,
            "isLayover": False,
            "isDelayed": False,
            "timeProcessed": "2018-06-02 07:59:10.59",
            "tripShortName": "8078058",
            "routeShortName": "N",
            "schedAdhMsec": 4468229,
            "schedAdh": "74.5 minutes (late)",
            "headwayMsec": 1898655,
            "scheduledHeadwayMsec": 300000,
            "previousVehicleId": "1405",
            "previousVehicleSchedAdhMsec": -31776,
        },
        {
            "time": "2018-06-02 08:19:11.456",
            "lat": 37.77328,
            "lon": -122.39783,
            "speed": 0,
            "heading": 218,
            "vehicleId": "1410",
            "assignmentId": "9708",
            "timeProcessed": "2018-06-02 08:19:19.498",
        },
    ]

    sent_req = httpretty.last_request()
    assert sent_req.querystring["queryDate"] == ["10-01-2023"]
    assert sent_req.querystring["beginTime"] == ["07:50"]
    assert sent_req.querystring["endTime"] == ["08:20"]
    assert sent_req.querystring["vehicle"] == ["1410"]


def test_format_url():
    agency = "test_agency"
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    assert client._format_url(client.ARRIVAL_DEPARTURE_OBSERVATIONS) == (
        SwiftlyAPIClient.PROD_BASE_URL + "/otp/test_agency/arrivals-departures"
    )

    assert client._format_url(
        client.RUN_TIMES_BY_ROUTE,
        route_short_name="test_route",
    ) == (
        SwiftlyAPIClient.PROD_BASE_URL
        + "/run-times/test_agency/route/test_route/by-trip"
    )


@httpretty.activate
def test_get_routes():
    agency = "test_agency"
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    mock_url = client._format_url(client.ROUTES)

    httpretty.register_uri(
        httpretty.GET,
        mock_url,
        responses=[
            httpretty.Response(
                body="""
                    {
                      "data": {
                        "agencyKey": "sfmta",
                        "routes": [
                          {
                            "id": "13228",
                            "longName": "Judah",
                            "name": "N - Judah",
                            "shortName": "N",
                            "type": "0"
                          },
                          {
                            "id": "13221",
                            "longName": "Embarcadero",
                            "name": "Embarcadero",
                            "shortName": "E",
                            "type": "0"
                          },
                          {
                            "id": "13222",
                            "longName": "Market & Wharves",
                            "name": "F - Market & Wharves",
                            "shortName": "F",
                            "type": "0"
                          }
                        ]
                      },
                      "route": "/info/sfmta/routes GET",
                      "success": true
                    }
                    """,
                status=200,
            ),
        ],
    )

    routes = client.get_routes()

    assert routes == [
        {
            "id": "13228",
            "longName": "Judah",
            "name": "N - Judah",
            "shortName": "N",
            "type": "0",
        },
        {
            "id": "13221",
            "longName": "Embarcadero",
            "name": "Embarcadero",
            "shortName": "E",
            "type": "0",
        },
        {
            "id": "13222",
            "longName": "Market & Wharves",
            "name": "F - Market & Wharves",
            "shortName": "F",
            "type": "0",
        },
    ]


@httpretty.activate
def test_get_real_time_vehicles():
    agency = "test_agency"
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    mock_url = client._format_url(client.REAL_TIME_VEHICLES)

    httpretty.register_uri(
        httpretty.GET,
        mock_url,
        responses=[
            httpretty.Response(
                body="""
                    {
                      "success": true,
                      "route": "/real-time/alexandria-dash/vehicles GET",
                      "data": {
                        "agencyKey": "alexandria-dash",
                        "vehicles": [
                          {
                            "id": "0402",
                            "routeId": "KST",
                            "routeShortName": "KST",
                            "tripId": "440020",
                            "headsign": "Market Square/City Hall",
                            "vehicleType": "3",
                            "loc": {
                              "lat": 38.80572,
                              "lon": -77.05176,
                              "time": 1743435372,
                              "speed": 2.2352,
                              "heading": 99.77457
                            },
                            "nextStopId": "574",
                            "nextStopName": "King St + Patrick St",
                            "directionId": "1"
                          },
                          {
                            "id": "0523",
                            "routeId": "102",
                            "routeShortName": "102",
                            "tripId": "148020",
                            "headsign": "Alexandria West-Mark Center Station",
                            "vehicleType": "3",
                            "loc": {
                              "lat": 38.81411,
                              "lon": -77.07681,
                              "time": 1743435361,
                              "speed": 5.36448,
                              "heading": 275.32855
                            },
                            "nextStopId": "117",
                            "nextStopName": "Janneys Ln + E Taylor Run Pkwy",
                            "directionId": "0"
                          }
                        ]
                      }
                    }
                        
                    """,
                status=200,
            ),
        ],
    )

    vehicles = client.get_real_time_vehicles()
    vehicle_ids = [vehicle["id"] for vehicle in vehicles]

    assert vehicle_ids == ["0402", "0523"]


@httpretty.activate
def test_get_vehicles():
    agency = "test_agency"
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    mock_url = client._format_url(client.VEHICLES)

    httpretty.register_uri(
        httpretty.GET,
        mock_url,
        responses=[
            httpretty.Response(
                body="""
                    [
                        {
                            "id": 83900,
                            "externalId": "0096",
                            "vehicleGroupId": 146,
                            "vehicleType": null,
                            "nonPassenger": false,
                            "hasOa": false,
                            "capacity": null,
                            "crushCapacity": null,
                            "createdAt": "2022-10-05T00:12:00.285394Z",
                            "updatedAt": "2022-10-05T00:12:00.285394Z",
                            "lastReported": null,
                            "devicesUpdatedAt": null
                        },
                        {
                            "id": 83902,
                            "externalId": "0101",
                            "vehicleGroupId": 146,
                            "vehicleType": null,
                            "nonPassenger": false,
                            "hasOa": false,
                            "capacity": null,
                            "crushCapacity": null,
                            "createdAt": "2022-10-05T00:12:00.365857Z",
                            "updatedAt": "2022-10-05T00:12:00.365857Z",
                            "lastReported": null,
                            "devicesUpdatedAt": null
                        }
                    ]
                    """,
                status=200,
            ),
        ],
    )

    vehicles = client.get_vehicles()
    vehicle_ids = [vehicle["externalId"] for vehicle in vehicles]

    assert vehicle_ids == ["0096", "0101"]

@httpretty.activate
def test_get_missing_service_export_numeric_trip_ids():
    """
    Test that all-numeric trip IDs are preserved as strings,
    preventing type mismatch issues in downstream processing.
    """
    agency = "test_agency"
    target_date = date(2025, 8, 5)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    url = client._format_url(client.MISSING_SERVICE)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""\
service_date,trip_completion_status,trip_adjustments,trip_id,route_id,block_id,service_id,trip_short_name,route_short_name,vehicle_ids,driver_ids,direction_id,day_of_week,num_scheduled_stops,num_observed_stops
2025-08-05,MISSING,,1080,1,801,WD,,,,,0,3,25,0
2025-08-05,MISSING,,11080,1,802,WD,,,,,1,3,30,0
2025-08-05,PARTIAL,,13080,2,803,WD,Route 2,,123,,0,3,20,1
2025-08-05,PARTIAL,,138080,2,804,WD,,,456,789,1,3,15,2
                """,
                status=200,
            ),
        ],
    )

    df = client.get_missing_service_export(target_date)

    expected_df = pd.DataFrame(
        {
            "service_date": ["2025-08-05", "2025-08-05", "2025-08-05", "2025-08-05"],
            "trip_completion_status": ["MISSING", "MISSING", "PARTIAL", "PARTIAL"],
            "trip_id": ["1080", "11080", "13080", "138080"],
            "route_id": ["1", "1", "2", "2"],
            "block_id": ["801", "802", "803", "804"],
            "service_id": ["WD", "WD", "WD", "WD"],
            "vehicle_ids": [math.nan, math.nan, "123", "456"],
            "driver_ids": [math.nan, math.nan, math.nan, "789"],
            "direction_id": [0, 1, 0, 1],
            "day_of_week": [3, 3, 3, 3],
        }
    )

    # Compare selected columns to verify dtypes are correct
    assert df[
        [
            "service_date",
            "trip_completion_status",
            "trip_id",
            "route_id",
            "block_id",
            "service_id",
            "vehicle_ids",
            "driver_ids",
            "direction_id",
            "day_of_week",
        ]
    ].equals(expected_df)

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["08-05-2025"]
