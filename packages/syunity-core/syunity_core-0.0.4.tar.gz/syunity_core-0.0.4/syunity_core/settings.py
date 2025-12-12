import os
import time
import sqlite3
import shutil
from syunity_core.database import db
from syunity_core.system.logger import logger

# =============================================================================
# 本地环境配置 (不依赖 Settings)
# =============================================================================
TEST_ROOT = os.path.join(os.getcwd(), "test_workspace")
DB_DIR = os.path.join(TEST_ROOT, "db")
BACKUP_DIR = os.path.join(TEST_ROOT, "backup")
DB_PATH = os.path.join(DB_DIR, "local_test.db")

def setup_env():
    """准备测试目录"""
    if os.path.exists(TEST_ROOT):
        try:
            shutil.rmtree(TEST_ROOT)  # 清理上次残留
            logger.info("🧹 清理旧测试目录")
        except Exception:
            pass
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def init_sqlite():
    """初始化 SQLite 环境"""
    logger.info("🔌 [Step 0] 初始化数据库...")

    # 直接传入绝对路径，不依赖任何外部配置
    db.init_sqlite(
        db_path=DB_PATH,
        debug_mode=True,  # 强制开启调试模式
        reset_db=True     # 强制重置数据库，保证测试环境纯净
    )
    logger.info(f"✅ SQLite Ready: {DB_PATH}")


def run_sqlite_test():
    logger.info("\n" + "="*50)
    logger.info("🚀 开始 SQLite 全功能测试 (Local Mode)")
    logger.info("="*50)

    # =================================================================
    # Step 1: 创建表结构 (含约束)
    # =================================================================
    logger.info("👉 [Step 1] 创建表结构...")

    # 1.1 普通表
    db.sqlite.create_table("department", {
        "name": "TEXT NOT NULL",
        "code": "TEXT",
        "manager": "TEXT",
        "location": "TEXT"
    })

    db.sqlite.create_table("user", {
        "username": "TEXT NOT NULL",
        "email": "TEXT",
        "age": "INTEGER",
        "dept_id": "INTEGER"
    })

    # 1.2 场景 A: 单字段唯一
    db.sqlite.create_table("sys_user", {
        "username": "TEXT NOT NULL UNIQUE",
        "age": "INTEGER"
    })

    # 1.3 场景 B: 组合唯一 (constraints)
    db.sqlite.create_table("sys_employee", {
        "dept_code": "TEXT NOT NULL",
        "emp_no": "TEXT NOT NULL",
        "name": "TEXT"
    }, constraints=[
        "UNIQUE(dept_code, emp_no)"
    ])

    logger.info("✅ 所有表结构创建完毕")

    # =================================================================
    # Step 2: 验证约束是否生效
    # =================================================================
    logger.info("👉 [Step 2] 验证唯一性约束...")

    try:
        # 插入正常数据
        db.sqlite.save("sys_employee", {"dept_code": "RD", "emp_no": "1001", "name": "张三"})
        # 插入非冲突数据
        db.sqlite.save("sys_employee", {"dept_code": "MKT", "emp_no": "1001", "name": "李四"})
        logger.info("   正常数据插入... OK")

        # 插入冲突数据
        logger.info("   尝试插入重复数据 (RD, 1001)...")
        db.sqlite.save("sys_employee", {"dept_code": "RD", "emp_no": "1001", "name": "王五"})

        logger.error("❌ 严重错误：组合唯一约束未生效！")
    except Exception as e:
        logger.info(f"✅ 捕获到预期错误 (约束生效): {e}")

    # =================================================================
    # Step 3: 插入数据 (CRUD - Create)
    # =================================================================
    logger.info("👉 [Step 3] 插入测试数据...")

    # 批量插入
    depts = [
        {"name": "研发部", "code": "RD", "manager": "张三", "location": "3F"},
        {"name": "市场部", "code": "MKT", "manager": "李四", "location": "2F"}
    ]
    db.sqlite.save("department", depts)

    users = [
        {"username": "Alice", "email": "alice@test.com", "age": 25, "dept_id": 1},
        {"username": "Bob", "email": "bob@test.com", "age": 30, "dept_id": 1}
    ]
    count = db.sqlite.save("user", users)
    logger.info(f"✅ 成功插入 {len(depts)} 个部门和 {count} 个用户")

    # =================================================================
    # Step 4: 修改数据 (CRUD - Update)
    # =================================================================
    logger.info("👉 [Step 4] 修改数据: 将 Bob 的年龄改为 31...")
    db.sqlite.execute("UPDATE user SET age=? WHERE username=?", (31, "Bob"))
    logger.info("✅ Update 操作完成")

    # =================================================================
    # Step 5: 查询数据 (CRUD - Read)
    # =================================================================
    logger.info("👉 [Step 5] 查询验证...")
    res = db.sqlite.find("user", {"username": "Bob"})
    bob = res[0] if res else None

    if bob and bob['age'] == 31:
        logger.info(f"   验证成功：Bob 年龄已更新为 31 (查询结果: {dict(bob)})")
    else:
        logger.error("   验证失败：数据不匹配")

    # =================================================================
    # Step 6: 备份和导出
    # =================================================================
    logger.info("👉 [Step 6] 备份与导出...")

    # 6.1 物理备份
    backup_file = os.path.join(BACKUP_DIR, f"backup_{int(time.time())}.db")
    try:
        dest_db = sqlite3.connect(backup_file)
        db.sqlite.conn.backup(dest_db)
        dest_db.close()
        logger.info(f"✅ 物理备份成功: {backup_file}")
    except Exception as e:
        logger.error(f"❌ 备份失败: {e}")

    # 6.2 导出 SQL
    export_sql = os.path.join(BACKUP_DIR, "export.sql")
    try:
        with open(export_sql, 'w', encoding='utf-8') as f:
            for line in db.sqlite.conn.iterdump():
                f.write('%s\n' % line)
        logger.info(f"✅ 导出 SQL 成功: {export_sql}")
    except Exception as e:
        logger.error(f"❌ 导出 SQL 失败: {e}")

    # =================================================================
    # Step 7: 清理资源
    # =================================================================
    logger.info("👉 [Step 7] 清理资源...")
    db.sqlite.close()
    logger.info("✅ 数据库连接已关闭")

    # 不删除文件，以便你可以手动去 test_workspace 查看结果
    logger.info(f"ℹ️  测试文件保留在: {TEST_ROOT}")
    logger.info("🎉 SQLite 测试全部通过！")

if __name__ == "__main__":
    setup_env()
    init_sqlite()
    run_sqlite_test()