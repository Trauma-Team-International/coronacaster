<h1 align="center">
  <br>
  <a href="http://autonom.io"><img src="https://raw.githubusercontent.com/autonomio/coronacaster/master/assets/coronacaster_logo.png" alt="Coronacaster" width="250"></a>
  <br>
</h1>

<p align="center">
  <a href="#what">what?</a> •
  <a href="#why">why?</a> •
  <a href="#how">how?</a> •
  <a href="#start-forecasting">start forecasting</a> •
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

Coronacaster is an easy-to-use interface for performing a bayesian experiment to predict COVID-19 cases in any country. Typically you will follow three simple steps:

1) Plot country's cases and deaths as reference
2) Choose your model; `exp` or `polyN` (e.g. `poly1` for first order polynomial function)
3) Perform the experiment and review the results 

**Fig 1:** An example of forecasting result where we predict daily cases in Finland.

<img src=https://raw.githubusercontent.com/autonomio/coronacaster/master/assets/coronacaster_experiment_plot.png>

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

