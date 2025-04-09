from datetime import datetime, timedelta
import json
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from langchain_community.tools.amadeus.flight_search import AmadeusFlightSearch #, FlightSearchSchema

class FlightSearchSchema(BaseModel):
    """Schema for the AmadeusSearchTool tool."""

    originLocationCode: str = Field(
        description=(
            " The three letter International Air Transport "
            " Association (IATA) Location Identifier for the "
            " search's origin airport. "
        )
    )
    destinationLocationCode: str = Field(
        description=(
            " The three letter International Air Transport "
            " Association (IATA) Location Identifier for the "
            " search's destination airport. "
        )
    )
    departureDateTimeOrigin: str = Field(
        description=(
            " The departure datetime from the origin airport "
            " for the flight search in the following format: "
            ' "YYYY-MM-DDTHH:MM:SS", where "T" separates the date and time '
            ' components. For example: "2023-06-09T10:30:00" represents '
            " June 9th, 2023, at 10:30 AM. "
        )
    )
    departureDateTimeDestination: str = Field(
        description=(
            " The departure datetime from the destination airport "
            " for the flight search in the following format: "
            ' "YYYY-MM-DDTHH:MM:SS", where "T" separates the date and time '
            ' components. For example: "2023-06-09T10:30:00" represents '
            " June 9th, 2023, at 10:30 AM. "
        )
    )
    page_number: int = Field(
        default=1,
        description="The specific page number of flight results to retrieve",
    )


class AmadeusSearchTool(BaseTool):
    name: str = "Tool for searching for two-way flights between origin and destination airports."
    description: str = (
        " Use this tool to search for two-way flights between the origin and "
        " destination airports at a departure between an earliest and "
        " latest datetime. "
    )
    args_schema: Type[BaseModel] = FlightSearchSchema

    def _run(self, 
        originLocationCode: str,
        destinationLocationCode: str,
        departureDateTimeOrigin: str,
        departureDateTimeDestination: str,
        page_number: int = 1,
        ) -> str:
        # Implementation goes here
        print(f"Searching for flights between {originLocationCode} and {destinationLocationCode} from {departureDateTimeOrigin} to {departureDateTimeDestination}.")

        # PATCH
        from typing import TYPE_CHECKING
        TYPE_CHECKING = True
        from amadeus import Client
        AmadeusFlightSearch.model_rebuild()

        amadeus_tool = AmadeusFlightSearch()

        # Origin City Flight options
        departureDateTimeE = datetime.strptime(departureDateTimeOrigin, "%Y-%m-%dT%H:%M:%S").date()
        departureDateTimeL = departureDateTimeE + timedelta(hours=12)

        inputs = {
            'originLocationCode':originLocationCode,
            'destinationLocationCode':destinationLocationCode,
            'departureDateTimeEarliest':departureDateTimeE.strftime('%Y-%m-%dT%H:%M:%S'),
            'departureDateTimeLatest':departureDateTimeL.strftime('%Y-%m-%dT%H:%M:%S'),
            'page_number':page_number
        }
        list_flights = amadeus_tool.invoke (input=inputs)
        list_flights = list_flights[0:3] if len(list_flights) > 2 else list_flights
        # print(json.dumps(list_flights, indent=4))

        # Destination City Flight options
        departureDateTimeE = datetime.strptime(departureDateTimeDestination, "%Y-%m-%dT%H:%M:%S").date()
        departureDateTimeL = departureDateTimeE + timedelta(hours=12)

        inputs = {
            'originLocationCode':destinationLocationCode,
            'destinationLocationCode':originLocationCode,
            'departureDateTimeEarliest':departureDateTimeE.strftime('%Y-%m-%dT%H:%M:%S'),
            'departureDateTimeLatest':departureDateTimeL.strftime('%Y-%m-%dT%H:%M:%S'),
            'page_number':page_number
        }
        list_flights2 = amadeus_tool.invoke (input=inputs)
        list_flights2 = list_flights2[0:3] if len(list_flights2) > 2 else list_flights2
        list_flights.extend(list_flights2)
        # print(json.dumps(list_flights, indent=4))

        return json.dumps(list_flights)
