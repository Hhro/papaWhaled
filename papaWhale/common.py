from hashlib import md5

get_hash = lambda f: md5(open(f,"rb").read()).hexdigest()