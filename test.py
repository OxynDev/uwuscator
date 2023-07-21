import uwuscator

res = uwuscator.Obfuscator(debug=False).run()
open("out.py","w").write(res)