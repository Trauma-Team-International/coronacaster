<h1 align="center">
  <br>
  <a href="http://autonom.io"><img src="https://raw.githubusercontent.com/autonomio/coronacaster/master/assets/coronacaster_logo.png" alt="CoronaCaster" width="250"></a>
  <br>
</h1>

<p align="center">
  <a href="#what">what?</a> •
  <a href="#why">why?</a> •
  <a href="#how">how?</a> •
  <a href="#start-simulating">start simulating</a> •
  <a href="https://autonom.io">About Autonomio</a> •
  <a href="https://github.com/autonomio/ICUSIM/issues">Issues</a> •
  <a href="#License">License</a>
</p>
<hr>
<p align="center">
Coronacast is a probabilistic programming method for time-series forecasting of COVID-19 cases based on empirical data. 
</p>

<hr>

### What?

ICUSIM dramatically simplifies the process ICU demand, capacity, and fatality simulation. The simulation is based on a logic that closely resembles the current empirical understanding of the problem. The power of Monte Carlo simulation can be summarized in two points: 

- Input parameter ranges are based on empirical evidence
- There is no ambiquity in terms of results

**Fig 1:** An example of simulation result where we test how often peak daily demand for standard ICU capacity stays below 278 (the official forecast of THL in Finland). 

<img src=https://media.discordapp.net/attachments/696359200774684745/698103055803220019/9jMw10xwcwAAAABJRU5ErkJggg.png>

This allows the consumer of the information to establish their own point-of-view regarding how likely a certain outcome may be. The Monte Carlo method entirely takes away doubt from the question "given a range of parameters, how often so and so values appear".

<hr>

### Why?

There are very few reasonable forecasting methods for COVID-19 cases that are 100% based on what has actually happened and where validation is built-in. 

<hr>

### How?

coronacaster follows a straightforward logic:

- Data consist of cases and deaths for all countries from 1st of January, 2020
- An option between exponential and polynomial functions is provided
- Many countries yield meaningful results

The `coronacaster.forecast()` command accepts the following parameters:

name | type | description
--- | --- | --- 
`country` | str | Country name, if there is "countries" column in the data - else use "World or "" for all data
`data` | DataFrame | dataframe with "dates" (datetime) and "cases" columns - coses is the number of daily new cases
`ftype` | str | 'polyN' where N is a number between 0 and a few (don't try more than 10 or so - becomes quite slow) or  'exp'  for exponential
`samples` | int | number of samples to use
`startdate` | str | start date number
`enddate` | str | end date number
`limit` | int | take start date to be where cumulative count exceeds limit
`**kwargs` | float | model params if wanted to use (see models.py)

<hr>

### 💾 Install

Released version:

#### `pip install coronacaster`

Daily development version:

#### `pip install git+https://github.com/autonomio/coronacaster`

<hr>

### Start Forecasting

To run a simulation, you need two things:

- time-series data
- `coronacaster.forecast()` command

```
import coronacaster

data = coronacaster.get_data_from_eu()
coronacaster.forecast('Finland', data, startdate='2020-04-01')
```

As a reference, plot the country's data: 

```
coronacaster.plot_country('Finland', data)
```

<hr>

### 💬 How to get Support

| I want to...                     | Go to...                                                  |
| -------------------------------- | ---------------------------------------------------------- |
| **...troubleshoot**           | [GitHub Issue Tracker]                   |
| **...report a bug**           | [GitHub Issue Tracker]                                     |
| **...suggest a new feature**  | [GitHub Issue Tracker]                                     |
| **...get support**            | [GitHub Issue Tracker]  · [Discord Chat]                         |
| **...have a discussion**      | [Discord Chat]                                            |

<hr>

### 📢 Citations

If you use CoronaCaster for published work, please cite:

`Autonomio's CoronaCaster [Computer software]. (2020). Retrieved from http://github.com/autonomio/ICUSIM.`

<hr>

### 📃 License

[MIT License](https://github.com/autonomio/talos/blob/master/LICENSE)

[github issue tracker]: https://github.com/automio/coronacaster/issues
[discord chat]: https://discord.gg/55QDD9

