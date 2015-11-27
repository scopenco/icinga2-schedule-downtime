# icinga2-shedule-downtime

## Description

Run this script will turn off all notifications (sheduled downtime) for this server in monitoring system.
You should enable livestatus in Icinga2 settings.

Config file /etc/icinga2-schedule-downtime.conf:
```python
mon_host = 'icinga2.domain.com'
mon_port = 6558
```

## Usage

```bash
icinga2-schedule-downtime.py DOWNTIME_IN_MINS
```
Without arguments script will shedule downtime for 15 mins.

Example:
  sheduled downtime for 60 mins.
```bash
icinga2-schedule-downtime.py 60
```

## Requirements

* Mk Livestatus should be enabled in Icinga 2.

### Platforms
Tested only on CentOS / Debian / Ubuntu

## Autors
* Author:: Andrei Skopenko (andrei@skopenko.net)
