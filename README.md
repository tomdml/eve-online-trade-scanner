# eve-online-trade-scanner
EVE Online is a video game with a complex, player-driven economy. One of the key aspects of this economy is the market, where players can buy and sell items. Items do not automatically move when purchased, creating price differences across regions, which can be arbitraged.

This project uses OAuth2 and the EVE API to find profitable market trades across regions. It also contains a utility to rapidly update existing orders (In line with the EULA, of course).

For a while, I used this tool to trade upwards of 250 item types per day. At one point I was pulling in 100B ISK a month. 

Unfortunately, the game developer made changes to market tax that heavily discouraged the playstyle - So I'm quite happy to open source this tool as it doesn't generate a lot of profit nowadays.

You will need an EVE ESI API Key, which can be entered in sso_utils.py.

## Screenshots

Trade Finder Output

![Trade Finder output](https://i.imgur.com/RhXZ9h0.png)

Fast Order Update

![Fast Order Update output](https://i.imgur.com/UT2mcTq.mp4)
