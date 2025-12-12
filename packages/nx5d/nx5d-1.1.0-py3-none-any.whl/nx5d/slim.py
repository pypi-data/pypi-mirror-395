from nx5d.spice import FsSpiceRepository, MemorySpiceRepository, BranchView

import logging, json

logger = logging.getLogger("slim")

'''
Spice is always being managed at proposal level.

However, the "spice repository" is meant to be able to select a
specific spice (proposal subfolder) from a collection of proposals.

The general recipe when working with spice would be:

 - Define the spice location using the NX5D_SPICE_REPO env var
   (e.g. "..../{proposal}/spice", if your spice is in a subfolder
   of a proposal folder).

 - Make sure the _specific_ spice folder exists ("mkdir -p .../spice")

 - Use the SLIM CLI utility for spice management; try "slim ?" for help.
   Generally, what you want to do with SLIM is:

   - Check for help: "slim ?"

   - Check if SLIM sees your proposals: "slim proposals?"

   - List the spice for a specific proposal: "slim <proposal> list"
     Initially your proposal list will be empty (because there's nothing
     in the spice folder!)

   - Seed the spice for your speific proposal, by piping JSON data
     contents into SLIM: "cat data.json | slim <proposal> seed <handle>=<type> -"
     e.g. for KMC3 experimental info:
     "cat nx5d/examples/kmc3/exp_info_pilatus.json | \
        slim 252-cw32-13756-roessle seed exp_info=xrd/geometry -"

   - View spice from a specific anchor point (i.e. "scan" or "run"):
     "slim <proposal> view <anchor>" e.g.
     "slim 252-cw32-roessle-13756 view r0003"

   - Update spice / modify values:
     "slim <proposal> update <type>@<anchor> <key>=<value>".
     Note that updating happens not only at the specified anchor,
     but already where the spice type is anchored. For instance:
     if a spice named "offsets" is anchored at "r0001", but
     the update command refers to "offsets@r0023", the value of the
     parameter (e.g. "slim ... update offsets@r0023 theta=3.14")
     will be changed at "r0001", _not_ at "r0023". See also below.

   - Re-anchor a spice type:
     "slim <proposal> anchor <handle> <anchor>", e.g.
     "slim ... anchor offsets r0023"
  

'''

def _json_from_args(*args):
    # Transforms a list of arguments into a JSON object:
    #
    #   - if the first argument is a single '-',
    #     read JSON from stdin
    #
    #   - if an argument is key=value pair, we use that
    #     (parsing the 'value' string according to JSON rules,
    #     i.e. possibly nesting JSON data types)
    #
    #   - if artument is an existing file path, attempt to
    #     read JSON from the corresponding file
    #
    #   - otherwise collect arguments, concatenate them into
    #     a string, and parse the string argument as a
    #     JSON object

    if len(args) == 0:
        return {}

    if len(args) == 1 and args[0] == '-':
        return json.load(sys.stdin)

    import os, sys

    _xpl = {} ## explicit key=value entries in 'args'
    _ext = {} ## externally loaded
    _jstr = ""
    for a in args:
        s = a.split('=')
        if len(s) == 2:
            _xpl[s[0]] = json.loads(s[1])
        elif len(s) == 1:
            if os.path.exists(s[0]):
                with open(s[0]) as f:
                    _ext.update(json.load(f))
            else:
                _jstr += s[0]

    if len(_jstr) > 0:
        try:
            _ext.update(json.loads(_jstr))
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f'{_jstr[0:5]}...{_jstr[-5:]}: '
                               f'neither an existent file nor a valid JSON string: '
                               f'{e}')

    if len(_xpl) > 0:
        _ext.update(_xpl)

    return _ext
            

def _branch_by_address(collection, addr_spec):
    # Returns a spice branch from a collection, using an
    # address specification form the command line.
    # The address specification "addr_spec" can be either
    # a UUID, or a <handle>@<anchor> spec.

    if '@' in addr_spec:
        t, a = addr_spec.split('@')
        view = collection.view(a, t)
        target = view.data[t]
    else:
        cand = collection.find(startswith=True, insensitive=True, uuid=addr_spec)
        if len(cand)==1:
            target = cand[0]
        else:
            target = cand

    if not isinstance(target, BranchView):
        print(f'bad branch for "{addr_spec}": {target}')
        return -1

    return target


def _check_dry(args):
    if "--dry" in args:
        args.remove('--dry')
        return True
    return False


class Application:
    '''
    Main application model for 'sm', the 'Spice Manager'.
    '''
    def __init__(self, args=None, env=None):
        from os import environ
        from sys import argv
        self._args = args if args is not None else argv
        self._env = env if env is not None else environ

        url = self._env.get('NX5D_SPICE_REPO',
                            self._env.get('NX5D_DATA_REPO',
                                          'file://.'))

        fsrepo = FsSpiceRepository(url)
        if self._args[-1].startswith('--dry'):
            self._args = self._args[:-1]
            logger.info(f'Dry-run requested; write operations in-memory only.')
            self._repo = MemorySpiceRepository(fsrepo)
        else:
            self._repo = fsrepo


    def _doctitle(self, cmd):
        return ''.join([
            x.replace('\n', '') for x in  \
            getattr(self, f'_cmd_{cmd}').__doc__.split('\n')[0:2]
        ])


    def _docdetail(self, cmd):
        return '\n'.join(
            getattr(self, f'_cmd_{cmd}').__doc__.split('\n')[2:]
        )


    def _all_commands(self):
        return [
            c[5:] for c in \
            filter(lambda x: x.startswith('_cmd_'), self.__dir__())
        ]

    def help_and_exit(self, args):
        docstr = lambda x: self._doctitle(x)
        cmd_text = "\n".join([
            f"  {c:10s} {docstr(c)}" \
            for c in self._all_commands()
        ])
        help_text = \
            f"Usage: {self._args[0]} <proposal> <command> [<opts>...]\n"\
            f"\n"\
            f"Available commands:\n"\
            f"{cmd_text}\n"\
            f"\n"\
            f"Try `{self._args[0]} ? <command>` for detailed help on commands."
        print(help_text)
        return -1


    def command_help_and_exit(self, rest):
        if len(rest) == 0:
            return self.help_and_exit(self._args)
        cmd = rest[0]
        help_text = \
            f"{cmd}: {self._doctitle(cmd)}\n"\
            f"{self._docdetail(cmd)}"
        print(help_text)
        return -1


    def list_proposals(self, args):
        # This is used mostly for autocomplete of the first parameter
        print('\n'.join(
            filter((lambda x: x.startswith(args[0])) \
                   if len(args)>0 else lambda x: x,
                   self._repo.all())
        ))


    def list_commands(self, args):
        print('\n'.join(
            filter((lambda x: x.startswith(args[0])) \
                   if len(args)>0 else lambda x: x,
            self._all_commands())
        ))


    def list_anchors(self, pobj, args):
        '''
        Lists all anchor points (scans/runs) in a specific proposal
        '''
        print('\n'.join(pobj.anchors().keys()))


    def version_and_exit(self):
        print(f'Spice List Manager (slim) @ nx5d v{myver.version}')
        return 0


    def run(self):
        # Wrapper for ._run() to actually generate screen output
        r = self._run()
        if (r is not None) and type(r) != int:
            print(r)

        

    def _run(self):
        # Actual command that executes the application according to
        # the command line arguments.
        #
        # This returns a Python object (in most cases a string or
        # Pandas data object) which is then printed on the screen.
        # See .run() for a conveninent wrapper.
        #
        # The separation is done for better unit testing.
        
        if len(self._args) <= 1:
            return self.version_and_exit()

        if len(self._args)>=2:
            try:
                return {
                    '?': self.command_help_and_exit,
                    'help': self.command_help_and_exit,
                    '-h': self.command_help_and_exit,
                    'proposals?': self.list_proposals,
                    'commands?': self.list_commands,
                }[self._args[1]](self._args[2:])
            except KeyError:
                pass

        #try:
        proposal = self._repo.proposal(key=self._args[1])
        print(f'Proposal: {proposal.name}')
        #except AttributeError:
        #    print(f'No "{prop}" at "{self._repo.url_for(prop)}"')
        #    return -1

        try:
            action = self._args[2]
        except IndexError:
            self.list_anchors(pobj, self._args[1:])
            return -1

        proc = getattr(self, f"_cmd_{action}")

        if hasattr(proc, "__call__"):
            return proc(action, proposal, self._args[3:])


    def _rev_shortid(self, x):
        return x.meta('uuid')[:6]


    def _rev_conflict_list(self, rlist):
        return [
            self._rev_shortid(d) for d in \
            filter(lambda x: x.meta('revision') == rlist[0].meta('revision'), rlist)
        ]


    def _cmd_anchor(self, cmd, pobj, args):
        '''
        Anchors a spice branch at a new location

        Synopsis: anchor <anchor> <handle>

        Args:
        
          handle: handle (type) of the spice data
        
          anchor: new anchor point

        Returns: the UUID of the anchor entry, if successful.
        '''

        if len(args) != 2:
            print('Handle and anchor?')
            return -1

        anchor, handle = args
        try:
            n = pobj.anchor(anchor, handle)
        except Exception as e:
            print(e)
            return -1

        return n['uuid']
        

    def _cmd_seed(self, cmd, pobj, args):
        '''
        Create a spice branch from scratch
        
        The command will store the spice JSON file at the location of
        the configured repository.

        Synopsis: create <handle> -|<filename}|<p>=<v> [<p2>=<v2> ...]
        
        Args:
        
          handle: a Python-compatible string to identify
            the spice object by in autocomplete-sensitive environments
        
          p, v: key-value pairs representing the spice data,
            where "p" will always be interpreted as string, and "v"
            will be subject to an opportunistic cast (i.e. we try to
            convert it into "higher types" like int or float, but fall
            back to str if we fail).
        
          -: introduces an alternative way of specifying spice
            data; if this is the only parameter, spice data is read
            as a JSON package from stdin.

        Returns: the UUID of the seed entry, if successful.
        '''

        if len(args) < 2:
            print('Handle and values?')
            return -1

        handle = args[0]
        data = _json_from_args(*(args[1:]))
        try:
            n = pobj.seed(handle, data, idem=False)
        except Exception as e:
            print(e)
            return -1

        return n['uuid']


    def _cmd_update(self, cmd, pobj, args):
        '''
        Updates values for specified spice type, relative to anchor.

        If the latest available revision for the specified anchor is free
        of conflicts, it is used as a basis for a new revision. In the new
        revision, the fields specified are updated to the corresponding
        new values. A spice JSON file is sent to the repository to the same
        URL as the spice tree was read from.    

        Synopsis: update [--dry] <item> <field>=<value> [<field2>=<value> [...]],

        Args:

          item: a spice banch, designated either by its latest UUID,
            or by a <type>@<anchor> designation.

          field: name of the field to update

          value: the new value

        Returns: the UUID of the new entry, if successful.
        '''
        
        if len(args) == 0:
            print(f'{cmd}: item?')
            return -1

        try:
            if '@' in args[0]:
                # .update() receives (anchor, handle) as its address,
                # so we need to invert the order here
                addr = args[0].split('@')[::-1]
            else:
                # This is expected to be a UUID.
                addr = [uuid.UUID(args[0])]
            params = _json_from_args(*(args[1:]))
            n = pobj.update(*addr, payload=params)

        except Exception as e:
            print(e)
            return -1
        
        return n['uuid']
        

    def _cmd_list(self, cmd, pobj, args):
        '''
        List all anchor points and their associated spice handles

        Prints a list with spice handles as column heads, and anchor
        points as its index, will be displayed. The contents of the
        list are the first digits of single UUIDs if the respective
        revision is valid, or a list of UUIDs if there's a conflict.
        The listed UUIDs represent the spice entries in conflict.        
        
        Synopsis: list
        '''

        shortid = self._rev_shortid
        conflict_list = self._rev_conflict_list
        conflicted = lambda rlist: False if (len(rlist) <= 1) \
            else (rlist[0]['revision'] == rlist[1]['revision'])

        import pandas
        out = pandas.DataFrame()
        line_format = f'{{pinfo:{len(pobj.name)}s}}  {{anchor}}   {{handles}}'
        for anchor,dat in pobj.collection.anchors().items():
            cols = {
                'anchor': {anchor: anchor},
            }
            handles = {
                dat2[0]['handle']: {
                    anchor:
                        shortid(BranchView(dat2[0])) \
                        if not conflicted(dat2) \
                        else ','.join(
                            conflict_list([BranchView(d) for d in dat2])
                        )
                } \
                for handle,dat2 in dat.items()
            }
            cols.update(handles)
            out = pandas.concat([out, pandas.DataFrame(cols)], ignore_index=True)

        if len(out)>0:
            return out.set_index('anchor').fillna('')
        else:
            return None


    def _cmd_view(self, cmd, pobj, args):
        '''
        Lists the revision history for a specific anchor

        Synopsis: view <anchor> [<handle> [<handle> ...]]

        Args:
          anchor: Reference of a scan, representing the anchor point
            for which the view should be valid. This need not be the
            actual anchor point of a specific spice type -- if this
            is any other scan reference (even an unexistent one), the
            spice entries anchored directly above it will be considered.

          *handles: list of spice types to display; if the list is empty,
            all available types will be displayed.

        Returns: a table with anchor points, spice type, revision and
          a list of parameters will be displayed.
        '''
        if len(args)==0:
            print(f'{cmd}: anchor within "{pobj.name}"?')
            return -1

        anchor = args[0]
        handles = args[1:]

        try:
            view = pobj.view(anchor, *handles, ignore_conflict=True)
        except SpiceUnavailable as e:
            print(e)
            return -1

        return view._as_pandas_dframe().fillna('')


def main(args=None, env=None):
    from os import environ
    from sys import argv
    app = Application(args if args is not None else argv,
                      env if env is not None else environ)

    return app.run()
