CREATE TABLE "AirlineDelays" (
	"id" SERIAL NOT NULL,
    "year" INT   NOT NULL,
    "month" INT   NOT NULL,
    "carrier" VARCHAR(255)   NOT NULL,
    "carrier_name" VARCHAR(255)   NOT NULL,
    "airport" VARCHAR(255)   NOT NULL,
    "airport_name" VARCHAR(255)   NOT NULL,
    "arr_flights" FLOAT   NOT NULL,
    "arr_del15" FLOAT   NOT NULL,
    "carrier_ct" FLOAT   NOT NULL,
    "weather_ct" FLOAT   NOT NULL,
    "nas_ct" FLOAT   NOT NULL,
    "security_ct" FLOAT   NOT NULL,
    "late_aircraft_ct" FLOAT   NOT NULL,
    "arr_cancelled" FLOAT   NOT NULL,
    "arr_diverted" FLOAT   NOT NULL,
    "arr_delay" FLOAT   NOT NULL,
    "carrier_delay" FLOAT   NOT NULL,
    "weather_delay" FLOAT   NOT NULL,
    "nas_delay" FLOAT   NOT NULL,
    "security_delay" FLOAT   NOT NULL,
    "late_aircraft_delay" FLOAT   NOT NULL,
    CONSTRAINT "pk_AirlineDelays" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "AirportCodes" (
    "id" INT   NOT NULL,
    "country_code" VARCHAR(255)   NOT NULL,
    "iata" VARCHAR(255)   NOT NULL,
    "airport" VARCHAR(255)   NOT NULL,
    "latitude" FLOAT   NOT NULL,
    "longitude" FLOAT   NOT NULL,
    CONSTRAINT "pk_AirportCodes" PRIMARY KEY (
        "iata"
     )
);

ALTER TABLE "AirlineDelays" ADD CONSTRAINT "fk_AirlineDelays_airport" FOREIGN KEY("airport")
REFERENCES "AirportCodes" ("iata");