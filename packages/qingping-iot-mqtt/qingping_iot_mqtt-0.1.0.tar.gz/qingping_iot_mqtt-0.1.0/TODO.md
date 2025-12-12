# To-Do

## general roadmap

- [.] 1a - abstract classes and HEX protocol
- [.] 1b - CLI
- [.] 2 - MQTT connector and simple DB logging and VictoriaMetrics
- [.] 3 - JSON protocol
- [ ] 4 - device model
- [ ] 5 - HomeAssistant

## phase 1 - HEX

- [x] protocol, message, payloads, primitive interpretation
- [x] sensor readings from all types of reports - container, decoding
- [.] config - container, decoding RW, encoding W
- [ ] command - container, handle generic and re-provision (MQTT, Wi-Fi), encoding W
- [ ] reasonable CLI to handle all of that

## phase 2 - MQTT and simple DB logging

- [x] connector to broker - R
- [x] SQLite connector and logging - storing events and raw
- [ ] SQLite connector - parsing replays
- [ ] CLI for W
- [.] VictoriaMetrics

## phase 3 - JSON

- [.] protocol, message, payloads, primitive interpretation
- [ ] sensor readings from all types of reports - container, decoding
- [ ] config - container, decoding RW, encoding W
- [ ] command - container, handle generic and re-provision (MQTT, Wi-Fi), encoding W
- [ ] reasonable CLI to handle all of that

## phase 4 - device model

- [x] basic DeviceModel for config
- [ ] move DeviceModel to DeviceModelConfig and implement DeviceModel itself with proper link to protocol and abstract methods to get data
