%查看python版本
pyversion

% 重新加载python
clear classes;
mod=py.importlib.import_module('migration');
py.importlib.reload(mod);

% 调用python命令
py.migration.download_data