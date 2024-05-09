```shell
which runoak
```

> /home/mark/.cache/pypoetry/virtualenvs/context-collaboration-meDaFbyk-py3.10/bin/runoak

```shell
cat /home/mark/.cache/pypoetry/virtualenvs/context-collaboration-meDaFbyk-py3.10/bin/runoak
```

```python
#!/home/mark/.cache/pypoetry/virtualenvs/context-collaboration-meDaFbyk-py3.10/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from oaklib.cli import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```


See also
- https://github.com/INCATools/ontology-access-kit/blob/main/src/oaklib/cli.py

----

```shell
find ~ -name envo.db
```

* /home/mark/gitrepos/nmdc-ontology/downloads/envo.db
* /home/mark/gitrepos/semantic-sql/envo.db
* /home/mark/biosample_etc_database/envo.db
* /home/mark/.data/oaklib/envo.db

```shell
runoak cache-ls
```

> [pystow] ls -al /home/mark/.data/oaklib
> total 1981452

* drwxrwxr-x 2 mark mark       4096 May  3 20:57 .
* drwxrwxr-x 4 mark mark       4096 Feb 16 11:08 ..
* -rw-rw-r-- 1 mark mark    3637248 Mar 29 17:04 aio.db
* -rw-rw-r-- 1 mark mark     775706 Mar 29 17:04 aio.db.gz
* -rw-rw-r-- 1 mark mark  106467328 Feb 16 14:59 drugbank.db
* -rw-rw-r-- 1 mark mark   19696744 Feb 16 14:59 drugbank.db.gz
* -rw-rw-r-- 1 mark mark   77246464 May  3 20:57 envo.db
* -rw-rw-r-- 1 mark mark   14895192 May  3 20:57 envo.db.gz
* -rw-rw-r-- 1 mark mark  394846208 Feb 16 14:59 mesh.db
* -rw-rw-r-- 1 mark mark   87556908 Feb 16 14:59 mesh.db.gz
* -rw-rw-r-- 1 mark mark 1114869760 Feb 16 14:59 mondo.db
* -rw-rw-r-- 1 mark mark  208981682 Feb 16 14:59 mondo.db.gz


