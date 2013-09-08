slDeparturesCLI
===============

Simple commandline script to fetch station departures info for the Stockholm public transport system (SL)

Using this api: http://www.trafiklab.se/api/sl-realtidsinfo/

Example usage
===============
By name:
`slDeparturesCLI --stationstr=Stadshagen`

By id:
`slDeparturesCLI 9102`

Filtering by types:
`slDeparturesCLI 9192 --types=train --types=metro`

Limiting by amount:
`slDeparturesCLI 9192 --maxdepartures=5`

Conky:

    Stadshagen:
    ${execpi 60 slDeparturesCLI --conky --stationstr=Stadshagen}
        
    KTH:
    ${execpi 60 slDeparturesCLI --conky 9204}


TODO
===============
* Better functionality for stationstr searches.
* Conky formatting (`--conky`)
