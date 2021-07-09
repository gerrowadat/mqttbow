class PluginError(Exception):
    pass


class PluginUsageError(PluginError):
    pass


class Plugin(object):
    pass


class Print(Plugin):
    async def run(self, ki, args):
        if 'msg' not in args:
            raise PluginUsageError('must specify "msg" to plugins.Print')
        print(args['msg'])


class Led(Plugin):
    async def run(self, ki, args):
        if 'op' not in args:
            raise PluginUsageError('must specify "op" to plugins.Print')
        if args['op'] == 'clear':
            await ki.all_leds_off()
            return

        # all below require 'key'. Colour defaults to #ffffff
        if 'key' not in args:
            raise PluginUsageError('no key specified for "%s"' % (args['op']))

        if args['op'] == 'off':
            await ki.led_off(args['key'])

        if 'colour' not in args:
            args['colour'] = 'ffffff'

        if args['op'] == 'on':
            await ki.led_on(args['key'], args['colour'])

        if args['op'] == 'toggle':
            await ki.led_toggle(args['key'], args['colour'])

