# Introduce
A5赛题

postmantest.py 为主程序

**目前已实现:**
1. 登陆注册+人脸登陆注册 (缺少忘记密码/修改密码)
2. ai问答助手

## Depedency
```

```

## Error Fixs
1. 项目问题
  
长期以来我就是通过导入包完成main.py的功能实现，但是比如说我修改了一个小功能以后，单独运行anti_spoof.py时,导入的包就会报错，我想知道为什么？以及我应该如何避免这样的问题

解决方法：
```python
# 获取当前脚本所在的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, 'config', 'config.ini')
```

## git问题
撤销最近的提交
```shell
git reset
```