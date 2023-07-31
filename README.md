# Lambda Listener

A simple script to periodically check [lambda labs]() instance availability. It will play an alarm (`alarm.wav`) when a specified instance is found to be available.

## Usage:

Go into `listener.py` and add your desired instance types and regions to the `types` and `region` lists respectively.
Aquire an API key from Lambda Labs and put it in `./key.env`

Run:

```
python listener.py --keyfile ./key.env --sleep 1
```

This will run the listener using a key located at `./key.env` and would sleep 1 minute between checks