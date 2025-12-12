# gbp-feeds

This is a [Gentoo Build
Publisher](https://github.com/enku/gentoo-build-publisher) plugin for
publishing Atom and RSS feeds for builds.

## Features

You can retrieve Feeds for all builds on the GBP server or individual
machines.  For example, the Atom for all machines will have the URL
`/feeds.atom`.  The URL for the feed for the machine "babette" would be
`/machines/babette/feed.atom`. For RSS feeds, replace `.atom` with `.rss`.

Currently the output for each feed item pretty much looks like the output from
`gbp status`.

![screenshot](https://raw.githubusercontent.com/enku/screenshots/refs/heads/master/gbp-feeds/gbp-feeds.png)

## Installation

This is a server-side plugin, meaning to use gbp-feeds you must first install
the plugin on the GBP server. This assumes you already have a working Gentoo
Build Publisher installation. If not, refer to the GBP Install Guide first.

Install the gbp-fl package into the GBP instance:

```sh
cd /home/gbp
sudo -u gbp -H ./bin/pip install gbp-feeds
```

Restart the GBP web app.

```sh
systemctl restart gentoo-build-publisher-wsgi.service
```

## Usage

Once installed you can point your feed aggregator to your Gentoo Build
Publisher instance. For example, if the URL of your instance is
`http://10.1.45.11/` then the main RSS feed will be
`http://10.1.45.11/feed.rss`.  If you have builds for a machine named
"desktop" then the Atom feed for that machine will be
`http://10.1.45.11/machines/desktop/feed.atom`.
