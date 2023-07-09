bind = "0.0.0.0:5000"
accesslog = "-"
errorlog = "-"
reload = True
workers = 2
# https://docs.gunicorn.org/en/20.1.0/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
worker_tmp_dir = "/dev/shm"
access_log_format = '%(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
