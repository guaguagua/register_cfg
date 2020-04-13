### 1. 增加json文件错误配置检查
- 每个region的bit地址范围是否设置交叉了
- 每个region的bit地址范围是否超过了最大值
- 每个region，是否每个bit都说明了，没有用到的bit，写为reverse

### 2. 备份
- 根据日期备份 json文件，修改错误后可回滚

### 3. 用颜色区分不同的bit区域

### 4. 添加配置时，如果对应Addr有配置，需要提示是否 replace

### 5. 配置textEdit显示json文本美化

### 6. json.dumps() json.dump()的区别
[https://www.cnblogs.com/wswang/p/5411826.html](https://www.cnblogs.com/wswang/p/5411826.html)
