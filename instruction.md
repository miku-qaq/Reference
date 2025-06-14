`pip install flask requests openai pypinyin`
`pip install gunicorn gevent`

`gunicorn -w 4 -k gevent -b 0.0.0.0:80 app:app --timeout 120`
ip:8.148.67.80