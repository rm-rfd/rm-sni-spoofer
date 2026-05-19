py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

`python main.py` opens the control panel. It can edit `CONNECT_IP`, `FAKE_SNI`, `VLESS_URL`, `XRAY_SOCKS_PORT`, `XRAY_HTTP_PORT`, and `XRAY_LOG_LEVEL`, then save them back to `config.json` and show relay logs. `VLESS_URL` accepts `vless://` and `trojan://` share links, and the remote port must be `443`.

to run the relay without the gui:
python main.py --headless

to install packages using a proxy:
$env:HTTP_PROXY  = "http://127.0.0.1:10909"
$env:HTTPS_PROXY = "http://127.0.0.1:10909"
pip install -r requirements.txt

to build a distributable folder with the bundled xray binary:
pip install -r requirements-build.txt
python build.py
