# SPDX-License-Identifier: MIT
"""ttstart

 Time Trial starter console

 Optional configuration is via metarace sysconf under section "ttstart":

 key           | (type) description [default]
 ---           | ---
 topic         | (string) telegraph topic for start list updates [startlist]
 fullscreen    | (boolean) run application fullscreen after initialisation
 backlightdev  | (string) sysfs path to backlight device [null] (1)
               |          eg: /sys/class/backlight/acpi_video0
 backlightlow  | (float) dimmed backlight level between starters [0.25]
 backlighthigh | (float) backlight level during countdown [1.0]
 startlist     | (string) filename for a csv startlist file [startlist.csv]
 syncthresh    | (float) maximum allowed audio de-sync in seconds [0.12] (2)
 
 
 Notes:

   1.  The backlight brightness file in sysfs must be writable in order
       for dimming to work

   2.  The acoustic start signal is terminated if it is not playing
       in sync with the displayed countdown.

   3.  On 32 bit atom systems, it may be necessary to remove pulseaudio
       in order to get working sound output via gstreamer/playbin

       # apt remove 'pulseaudio*'

"""
__version__ = '1.0.3'

import sys
import gi
import logging
import metarace
import csv
import os
import cairo
import json
from importlib.resources import files
from metarace import telegraph
from metarace import tod
from metarace import jsonconfig

gi.require_version("GLib", "2.0")
from gi.repository import GLib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version("Gdk", "3.0")
from gi.repository import Gdk

gi.require_version('Pango', '1.0')
from gi.repository import Pango

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

gi.require_version('Gst', '1.0')
from gi.repository import Gst

PRGNAME = 'org._6_v.ttstart'
APPNAME = 'TTStart'

_DEFTOPIC = 'startlist'
_DEFAUDIOSYNCTHRESH = 0.15
_RESOURCE_PKG = 'ttstart'
_SOUNDFILE = 'start.wav'
_STARTLIST = 'startlist.csv'
_TIMEFONT = 'TeXGyreHerosCn Bold '
_COUNTERFONT = 'TeXGyreHerosCn Bold '
_NOHDR = ['Start', 'start', 'time', 'Time', '']
_LOGLEVEL = logging.DEBUG
_log = logging.getLogger('ttstart')
_log.setLevel(_LOGLEVEL)
_PANGO_SCALE = float(Pango.SCALE)


def _json_hook(obj):
    """De-serialise tod objects."""
    if '__tod__' in obj:
        return tod.mktod(obj['timeval'])
    elif '__agg__' in obj:
        return tod.mkagg(obj['timeval'])
    return obj


def _fit_cent(cr, pr, h, w, msg, charHeight, fontName, pagew, ellipsize=True):
    """Fit msg centered on page at h in a box of width w."""
    if msg is not None:
        cr.save()
        l = Pango.Layout.new(pr)
        l.set_alignment(Pango.Alignment.CENTER)
        if ellipsize:
            l.set_ellipsize(Pango.EllipsizeMode.END)
        l.set_font_description(
            Pango.FontDescription(fontName + str(charHeight)))
        l.set_text(msg, -1)
        l.set_width(int(w * _PANGO_SCALE))
        l.set_height(0)
        cr.move_to(0.5 * (pagew - w), h)
        PangoCairo.update_context(cr, pr)
        l.context_changed()
        PangoCairo.show_layout(cr, l)
        cr.restore()


def _tod2key(tod=None):
    """Return a key from the supplied time of day."""
    ret = None
    if tod is not None:
        ret = int(tod.truncate(0).timeval)
    return ret


class ttstart(Gtk.Window):
    """GTK Time Trial Starter Console"""

    def __init__(self):
        _log.info('TT Start - Init')
        Gtk.Window.__init__(self, title='TT Start')

        # I/O telegraph
        self._io = telegraph.telegraph()
        self._io.setcb(self._tcb)
        self._topic = 'startlist'

        # Audio output
        self._player = Gst.ElementFactory.make('playbin', 'player')
        self._player.set_property('audio-sink',
                                  Gst.ElementFactory.make('alsasink', 'sink'))
        self._player.set_property(
            'video-sink', Gst.ElementFactory.make('fakesink', 'fakesink'))

        # there's a 32 bit overflow somewhere in gst, for now ignore the bus
        #bus = self._player.get_bus()
        #bus.add_signal_watch()
        #bus.connect('message', self._gst_message)

        # runstate
        self._running = True
        self._fullscreen = False
        self._width = 0
        self._height = 0
        self._areaW = 0
        self._areaH = 0
        self._backlight = 0.0
        self._backlightmax = 0
        self._backlightdev = None
        self._backlightlow = 0.25
        self._backlighthigh = 1.0
        self._syncthresh = 0.12
        self._countdown = None
        self._riderstr = None
        self._bulb = None
        self._currider = None
        self._tod = None
        self._nc = None
        self._ridermap = {}

        # Add the Drawing Area
        self._area_src = None
        self._area = Gtk.DrawingArea()
        self._area.connect('configure-event', self._configure)
        self._area.connect('draw', self._draw)
        self._area.set_size_request(400, 300)
        self.add(self._area)
        self._area.show()

        # Connect callbacks
        self.connect('destroy', self._window_destroy)

    def run(self):
        """Prepare the ttstart application and start telegraph."""
        self._io.start()
        self._loadconfig()
        if self._topic:
            self._io.subscribe(self._topic)
        self.show()
        self._tod = tod.now().truncate(0)
        self._nc = self._tod + tod.tod('1.21')
        GLib.timeout_add(2000, self._timeout)
        GLib.timeout_add_seconds(5, self._delayed_cursor)
        _log.debug('Starting clock at: %s', self._nc.rawtime(3))

    def _window_destroy(self, window):
        """Handle destroy signal."""
        _log.debug('Handle destroy cb')
        self._running = False
        self.hide()
        self._cancel_audio()
        self._player = None
        self._io.exit()
        Gtk.main_quit()

    def _configure(self, area, event, data=None):
        """Handle the drawing area configure event"""
        self._init_surface(area)
        self._redraw()
        return False

    def _draw(self, area, context):
        """Handle the drawing area 'draw' event"""
        if self._area_src is not None:
            context.set_source_surface(self._area_src, 0.0, 0.0)
            context.paint()
        else:
            _log.error('Drawing surface not yet configured')
        return False

    def _init_surface(self, area):
        """Re-allocate cairo surface when required"""
        newW = area.get_allocated_width()
        newH = area.get_allocated_height()
        if newW > self._areaW or newH > self._areaH:
            if self._area_src is not None:
                self._area_src.finish()
                self._area_src = None
            newW = max(self._areaW, newW)
            newH = max(self._areaH, newH)
            self._area_src = cairo.ImageSurface(cairo.FORMAT_ARGB32, newW,
                                                newH)
            _log.debug('Created new cairo surface %d x %d', newW, newH)
            self._areaW = newW
            self._areaH = newH
        self._width = newW
        self._height = newH

    def _redraw(self):
        """Request redraw on the cairo surface"""
        cr = cairo.Context(self._area_src)
        pr = PangoCairo.create_context(cr)
        self._do_drawing(cr, pr)
        self._area_src.flush()

    def _do_drawing(self, cr, pr):
        """Perform required drawing operations on the provided contexts"""
        cr.identity_matrix()

        # bg filled
        cr.set_source_rgb(0.85, 0.85, 0.90)
        cr.paint()

        # countdown box
        cbh = 0.56 * self._height
        cbw = 0.98 * self._width
        cbxo = 0.5 * (self._width - cbw)
        cbho = 0.5 * (self._height - cbh)
        cr.rectangle(cbxo, cbho, cbw, cbh)
        cr.set_source_rgb(0.92, 0.92, 1.0)
        cr.fill()

        # time string txt
        cr.set_source_rgb(0.1, 0.1, 0.1)
        if self._tod is not None:
            oh = -0.02 * self._height
            ch = 0.12 * self._height
            _fit_cent(cr, pr, oh, 0.95 * self._width, self._tod.meridiem(), ch,
                      _TIMEFONT, self._width, False)

        # countdown txt
        if self._countdown is not None:
            ctx = ''
            if self._countdown >= 0:
                ctx = str(self._countdown)
            else:
                ctx = '+' + str(-self._countdown)
            oh = 0.04 * self._height
            ch = 0.46 * self._height
            _fit_cent(cr, pr, oh, 0.95 * self._width, ctx, ch, _COUNTERFONT,
                      self._width, False)

        # rider name txt
        if self._riderstr is not None:
            oh = 0.78 * self._height
            ch = 0.10 * self._height
            _fit_cent(cr, pr, oh, 0.95 * self._width, self._riderstr, ch,
                      _COUNTERFONT, self._width)

        # starter bulbs
        if self._bulb is not None:
            rad = 0.14 * self._height
            oh = 0.5 * self._height
            ow = 0
            if self._bulb == 'red':
                ow = 0.15 * self._width
                cr.set_source_rgb(1.0, 0.2, 0.2)
            elif self._bulb == 'green':
                ow = 0.85 * self._width
                cr.set_source_rgb(0.2, 1.0, 0.2)
            cr.move_to(ow, oh)
            cr.arc(ow, oh, rad, 0, 6.3)
            cr.fill()

    def _clear(self):
        """Clear elements"""
        self._countdown = None
        self._riderstr = None
        self._bulb = None

    def _loadconfig(self):
        """Load config"""
        cr = jsonconfig.config({
            'ttstart': {
                'topic': _DEFTOPIC,
                'fullscreen': False,
                'backlightlow': 0.25,
                'backlighthigh': 1.0,
                'backlightdev': None,
                'syncthresh': _DEFAUDIOSYNCTHRESH,
                'startlist': _STARTLIST
            }
        })
        cr.add_section('ttstart')
        cr.merge(metarace.sysconf, 'ttstart')

        # set fullscreen
        if cr.get_bool('ttstart', 'fullscreen'):
            _log.debug('Fullscreen set')
            self._fullscreen = True
        else:
            _log.debug('Fullscreen not set')

        # load backlight parameters
        self._backlightdev = cr.get('ttstart', 'backlightdev')
        self._backlightlow = cr.get_float('ttstart', 'backlightlow', 0.25)
        self._backlighthigh = cr.get_float('ttstart', 'backlighthigh', 1.0)
        if self._backlightdev and os.path.exists(self._backlightdev):
            try:
                with open(os.path.join(self._backlightdev,
                                       'max_brightness'), ) as bf:
                    mbstr = bf.read()
                    self._backlightmax = int(mbstr)
                    self._backlightdev = os.path.join(self._backlightdev,
                                                      'brightness')
                    _log.info(
                        'Using backlight dev %r; max=%r, low=%d%%, high=%d%%',
                        self._backlightdev, self._backlightmax,
                        int(100.0 * self._backlightlow),
                        int(100.0 * self._backlighthigh))
            except Exception as e:
                _log.error('%s reading from backlight device: %s',
                           e.__class__.__name__, e)
                self._backlightdev = None
        else:
            _log.info('Backlight control not configured.')
            self._backlightdev = None
        # audio sync thresh
        self._syncthresh = abs(
            cr.get_float('ttstart', 'syncthresh', _DEFAUDIOSYNCTHRESH))
        _log.info('Audio sync threshold set to: %0.3fs', self._syncthresh)

        # set the control topic
        self._topic = cr.get('ttstart', 'topic')

        # load a sound file (must be in metarace defaults path)
        audioFile = os.path.join(metarace.DEFAULTS_PATH, _SOUNDFILE)
        if not os.path.exists(audioFile):
            _log.debug('Audio file not available, using resource file')
            sf = files(_RESOURCE_PKG).joinpath(_SOUNDFILE)
            with sf.open('rb') as f:
                with open(audioFile, 'wb') as g:
                    g.write(f.read())
                _log.debug('Wrote audio file %r', audioFile)
        else:
            _log.debug('Using %r for audio file', audioFile)
        self._player.set_property('uri', 'file://' + audioFile)

        # load riders (may be from CWD)
        datafile = metarace.default_file(cr.get('ttstart', 'startlist'))
        if os.path.exists(datafile):
            count = 0
            try:
                rlist = []
                with open(datafile) as f:
                    cr = csv.reader(f)
                    for r in cr:
                        st = None
                        bib = ''
                        series = ''
                        name = ''
                        # load rider info (ignore cat)
                        # start, no, series, name, cat
                        if len(r) > 0 and r[0] not in _NOHDR:
                            st = tod.mktod(r[0])
                            if len(r) > 1:  # got bib
                                bib = r[1]
                            if len(r) > 2:  # got series
                                series = r[2]
                            if len(r) > 3:  # got name
                                name = r[3]
                            if st is not None:
                                # enough data to add a starter
                                count += 1
                                nr = (st, bib, series, name)
                                rlist.append(nr)
                            else:
                                _log.warning('Ignored invalid starter %r', r)
                _log.info('Read %d entries from %r', count, datafile)
                self._newStartlist(rlist)
            except Exception as e:
                _log.warning('%s loading from startlist: %s',
                             e.__class__.__name__, e)

    def _cancel_audio(self):
        """Force audio player to null state"""
        self._player.set_state(Gst.State.NULL)
        return False

    def _delayed_cursor(self):
        """Remove the mouse cursor from the text area and go fullscreen"""
        cursor = Gdk.Cursor.new_for_display(Gdk.Display.get_default(),
                                            Gdk.CursorType.BLANK_CURSOR)
        self.get_window().set_cursor(cursor)
        if self._fullscreen:
            self.fullscreen()

        # run a start signal sanity check
        self._player.set_state(Gst.State.PLAYING)
        GLib.timeout_add_seconds(2, self._cancel_audio)
        return False

    def _check_play_pos(self, expect):
        """Check and handle audio offset."""
        try:
            postype, curpos = self._player.query_position(Gst.Format.TIME)
            if postype:
                err = float(abs(expect - curpos)) * 1e-9
                if err > self._syncthresh:
                    _log.error('Audio offset ~%0.3fs', err)
                    self._cancel_audio()
                else:
                    pass
                    #_log.debug('Audio offset ~%0.3fs', err)
        except Exception as e:
            _log.error('%s reading audio offset: %s', e.__class__.__name__, e)
        return False

    def _timeout(self, data=None):
        """Handle timeout"""
        if not self._running:
            return False
        try:
            ntime = tod.now()
            ntod = ntime.truncate(0)
            if ntime >= self._nc.truncate(1):
                self._tod = ntod
                self._nc += tod.ONE
                self._process_timeout()
            else:
                _log.debug('Timeout called early: %s', ntime.rawtime())
                # no need to advance, desired timeout not yet reached
        except Exception as e:
            _log.error('%s in timeout: %s', e.__class__.__name__, e)

        # Re-Schedule
        tt = tod.now() + tod.tod('0.01')
        while self._nc < tt:  # ensure interval is positive
            if tod.MAX - tt < tod.ONE:
                _log.debug('Midnight rollover')
                break
            _log.debug('Missed an interval, catching up')
            self._nc += tod.ONE
        ival = int(1000.0 * float((self._nc - tod.now()).timeval))
        GLib.timeout_add(ival, self._timeout)
        return False

    def _set_backlight(self, percent=None):
        """Attempt to adjust screen brightness between riders."""
        if self._backlightdev and abs(percent - self._backlight) > 0.05:
            if percent < 0.0:
                percent = 0.0
            elif percent > 1.0:
                percent = 1.0
            nb = int(0.5 + percent * self._backlightmax)
            try:
                with open(self._backlightdev, 'w') as f:
                    f.write(str(nb))
            except Exception as e:
                _log.error('%s writing backlight: %s', e.__class__.__name__, e)
            self._backlight = percent

    def _process_timeout(self):
        """Process countdown, redraw display."""
        curoft = _tod2key(self._tod)
        if self._currider is not None:
            cdn = self._currider - curoft
            if cdn == 10:
                self._player.set_state(Gst.State.PLAYING)
                rm = self._ridermap[self._currider]
                self._riderstr = '\u2004'.join((rm[1], rm[3]))
                self._bulb = 'red'
                _log.debug('Player started for: %s', self._riderstr)
            elif cdn in [8, 7, 6]:  # check audio stream sync
                self._check_play_pos(int((10 - cdn) * 1e9))
            elif cdn == 15:
                self._player.set_state(Gst.State.PAUSED)
                rm = self._ridermap[self._currider]
                self._riderstr = '\u2004'.join((rm[1], rm[3]))
                self._bulb = 'red'
                self._set_backlight(self._backlighthigh)
            elif cdn == 50 or cdn == 24:
                rm = self._ridermap[self._currider]
                self._riderstr = '\u2004'.join((rm[1], rm[3]))
                self._bulb = 'red'
                _log.info('LOAD: %s', self._riderstr)
            elif cdn == 30:
                self._set_backlight(self._backlighthigh)
            elif cdn == 5:
                pass
            elif cdn == 0:
                self._bulb = 'green'
                self._countdown = 0
                _log.info('GO: %s', self._riderstr)
            elif cdn == -4:  # load sets minimum gap-> ~25sec
                self._set_backlight(self._backlightlow)
                self._clear()  # note also removes the bulb
                self._currider = self._ridermap[self._currider][4]
                self._cancel_audio()
            if cdn >= 0 and cdn <= 30:
                if self._bulb:
                    self._countdown = cdn
                else:
                    self._countdown = None
            else:
                if cdn < 0 and cdn > -5:
                    self._countdown = cdn
                else:
                    self._countdown = None
        else:
            self._clear()
            self._riderstr = ''
        self._redraw()
        self._area.queue_draw()

    def _gst_message(self, bus, message):
        """Handle a Gst bus message"""
        t = message.type
        if t == Gst.MessageType.EOS:
            self._cancel_audio()
            _log.debug('gst EOS')
        elif t == Gst.MessageType.ERROR:
            self._cancel_audio()
            err, debug = message.parse_error()
            _log.error('gst error: %r/%r', err, debug)
        else:
            pass

    def _newStartlist(self, startlist=[]):
        """Re-load the startlist"""
        _log.debug('Re-loading startlist')
        self._ridermap = {}
        rlist = []
        for r in startlist:
            if len(r) > 3:
                st = tod.mktod(r[0])
                if st is not None:
                    key = _tod2key(st)
                    if key not in self._ridermap:
                        bib = r[1]
                        series = r[2]
                        name = r[3]
                        next = None
                        nr = [st, bib, series, name, next]
                        self._ridermap[key] = nr
                        rlist.append(key)
                    else:
                        _log.warning('Ignored duplicate start time: %r', r)
                else:
                    _log.warning('Ignoring invalid starter %r', r)
            else:
                _log.warning('Ignoring invalid starter %r', r)

        # sort startlist and build list linkages
        curoft = _tod2key(tod.now())
        self._currider = None
        rlist.sort()
        prev = None
        firstStart = '[n/a]'
        for r in rlist:
            if prev is not None:
                self._ridermap[prev][4] = r  # prev -> next
            prev = r
            if self._currider is None and r > curoft:
                self._currider = r
                rvec = self._ridermap[r]
                stxt = tod.tod(r).meridiem()
                firstStart = stxt
                sno = rvec[1]
                sname = rvec[3]
        # log the state after running
        _log.info('Loaded %d starters, next start: %s', len(self._ridermap),
                  firstStart)
        # last link will be None
        self._clear()
        return False

    def _tcb(self, topic, message):
        """Handle a callback from telegraph"""
        try:
            #_log.debug('Telegraph msg: t=%r, m=%r', topic, message)
            if topic == self._topic:
                _log.debug('Decoding message payload')
                startlist = json.loads(message, object_hook=_json_hook)
                if startlist is not None:
                    GLib.idle_add(self._newStartlist, startlist)
            else:
                pass
        except Exception as e:
            _log.error('%s decoding json object: %s', e.__class__.__name__, e)


def main():
    """Run the TT start application"""
    chk = Gtk.init_check()
    if not chk[0]:
        print('Unable to init Gtk display')
        sys.exit(-1)

    ch = logging.StreamHandler()
    ch.setLevel(_LOGLEVEL)
    fh = logging.Formatter(metarace.LOGFORMAT)
    ch.setFormatter(fh)
    logging.getLogger().addHandler(ch)

    try:
        GLib.set_prgname(PRGNAME)
        GLib.set_application_name(APPNAME)
        Gtk.Window.set_default_icon_name(metarace.ICON)
    except Exception as e:
        _log.debug('%s setting property: %s', e.__class__.__name__, e)

    metarace.init()
    Gst.init()
    app = ttstart()
    app.run()
    return Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
