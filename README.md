# SCUM community master

How to put a SCUM server on the community master server, and how players see the community server
list in the game. Nothing in the game is modified, and this repository contains no game files.

## Supported versions

Currently the community master supports **SCUM 0.6.13** (build 40038), for both the dedicated
server and the client.

Running a server of another SCUM version? Get in touch on our Discord,
[discord.gg/xMTq7EfMhS](https://discord.gg/xMTq7EfMhS), and we will add support for that version if
needed.

## Server owners

### 1. Point the server at the master

Edit `SCUM/Saved/Config/WindowsServer/ServerSettings.ini`. If it does not exist yet, start the
server once and stop it. Add at the end:

```ini
[SCUM.MasterServer]
Endpoint=51.68.190.110:31337
BanListEndpoint=51.68.190.110:31330
```

Start the server. Right after it boots it enrolls with the master and sends an update every 60 
seconds; it shows in the list
at once. `SCUM/Saved/Logs/SCUM.log` should contain:

```
LogMasterServerClient: Loaded master server endpoint: 51.68.190.110:31337
LogMasterServerClient: FMasterServerClient: EnrollServer
```

`Failed to receive response data` later in the log means the updates do not reach the master:
check that outgoing TCP to ports 31337 and 31330 is allowed, and the address.

The master lists the server under the public IP address its packets come from.

### 2. Open the ports

With the default `-port=7777`:

| Port | Protocol | Why |
|---|---|---|
| 7777 | UDP | game traffic |
| 7779 | TCP | join handshake; the list shows this port (game port + 2) |

For another game port, add 2 the same way. Open them in the server's firewall and, if the server
is behind NAT, forward them to it.

### 3. Check (Optional)

From the server machine, in the server's root folder:

```
python3 tools/check-master.py --port 7779
```

It checks the `ServerSettings.ini` section, that the master answers, and that the server is listed.

## Players

You need SCUM on your Steam account; Steam downloads the old version for owners only, and it must
be running while you play.

### 1. Download the 0.6.13 client

Steam keeps every released version and hands out an old one through its console. It saves such a
download in this folder:

```
C:\Program Files (x86)\Steam\steamapps\content\app_513710\depot_513711
```

(If Steam is installed elsewhere, it is `steamapps\content\app_513710\depot_513711` inside your
Steam folder.)

1. **Before downloading**, check whether that `depot_513711` folder already exists. It does if you
   ever downloaded an old SCUM version this way. If it exists, delete it: Steam writes the new
   download into it without removing the old files, and the game crashes on the mix of two
   versions.
2. Open the Steam console: press Win+R, enter `steam://open/console` and confirm. Steam opens a
   **Console** tab.
3. Paste this command and press Enter:

   ```
   download_depot 513710 513711 1424455789973759863
   ```

4. Wait. The download is about 70 GB and the console shows no progress bar. When it is done the
   console prints `Depot download complete`.
5. Move the `depot_513711` folder out of Steam's folder to a place of its own and give it a clear
   name, for example `C:\Games\SCUM-0.6.13`. This folder is your 0.6.13 client from now on; the
   steps below use it.

This does not touch your normal SCUM installation.

### 2. Install EasyAntiCheat for this version

Once, in your client folder (`C:\Games\SCUM-0.6.13` in the example), run `EasyAntiCheat\EasyAntiCheat_Setup.exe` and choose **Install** (or
run `EasyAntiCheat_Setup.exe install 171` from a command prompt). Without it the game reports
"File integrity compromised" and multiplayer stays disabled.

### 3. Start the game with the launcher

Copy [`client/Start-SCUM-0.6.13.bat`](client/Start-SCUM-0.6.13.bat) into the client folder (the one
holding `SCUM_Launcher.exe`) and always start the game with it. It points the game at the community
master on every start, so the in-game server browser lists the community servers, and starts the
game through the EasyAntiCheat launcher as the game requires. Starting `SCUM.exe` directly skips
EasyAntiCheat and disables multiplayer. `-NotInstalled` keeps this client's settings and saves in
its own folder, apart from your normal SCUM installation.

## Rules

The master operator can take a server off the list or block a machine. Fake player counts, attacks on
the master and impersonating other servers get a server removed.
