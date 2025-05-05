# The following Python source includes translatable strings using =_( )=
# convention, and produces the expected output when run :

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Change "fr" according to the language

import gettext
import os
import jinja2

fr = gettext.translation('fr', localedir='locale', languages=['fr'])
fr.install()
_ = fr.gettext

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'view')]),
   )

if __name__=='__main__':
  template = env.get_template('walkthrough.html')
  new = open("fr.html", "x")
  new.write(template.render(_ = _))
  new.close