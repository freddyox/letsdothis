const fs = require('fs');
const util = require('util');
const path = require('path');
const results = require('./results.json');

const generate = async () => {
  // Reduce results array to object keyed by event URL (without page param)
  const events = {};
  results.forEach(result => {
    const url = result.event_url.split('&pagenum=')[0];
    const event = events[url];
    if (event) {
      event.results.push(...result.results);
    } else {
      events[url] = result;
    }
  });

  // Split results array into races object by race title
  Object.keys(events).forEach(url => {
    const event = events[url];
    events[url] = {
      ...event,
      races: event.results.reduce((races, result) => {
        if (races[result.race_title]) {
          races[result.race_title].results.push(result);
          return races;
        }
        return {
          ...races,
          [result.race_title]: { results: [result] },
        };
      }, {}),
    };
    delete events[url].results;
  });

  Object.keys(events).forEach(async url => {
    const id = url.split('meetingid=')[1];
    await util.promisify(fs.writeFile)(path.join(`./events/${id}.json`), JSON.stringify(events[url]));
  });
};

generate();
