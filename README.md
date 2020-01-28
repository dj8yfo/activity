1. put your proxies -> **proxies.raw** at project root
2. you also need [morphs-swap/0ck2cj9LPpV.snip](morphs-swap/0ck2cj9LPpV.snip) , **morphs-swap/H1mZzivpAyZ.snip** , \
[morphs-swap/test/cGqBcnDzvC2.snip](morphs-swap/test/cGqBcnDzvC2.snip) files to assemble the puzzle 
3. start with [./prepare_env_a_bit.sh](prepare_env_a_bit.sh) 

```
...
CREATE USER 'sybil'@'localhost' IDENTIFIED BY 'morphs-swap/H1mZzivpAyZ.snip content';
...
CREATE DATABASE testdb;
...

./prepare_env_a_bit.sh

. $(pipenv --venv)/bin/activate
cd morphs-swap/

python -m scrapy crawl swap-fledge -a loc={loc} -a cat={cat} -a per_page={per_page}
python multirunner.py {start_index}  # alternatively, for a group of locations, categories
```

