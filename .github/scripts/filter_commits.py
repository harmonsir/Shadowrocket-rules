# filter_commits_safe.py
# 用法（在仓库目录下）:
# git filter-repo --force --refs <branch> --commit-callback "$(cat .github/scripts/filter_commits.py)"
#
import datetime as _dt


# 保留时限：90 天（可改）
CUTOFF_DAYS = 90
cutoff = (_dt.datetime.now() - _dt.timedelta(days=CUTOFF_DAYS)).date()


def _to_date(ts):
    # commit.committer_date 是 bytes like b'169...' 或 str 的 unix timestamp
    if isinstance(ts, bytes):
        ts = int(ts.decode().split()[0])
    else:
        ts = int(ts)
    return _dt.datetime.utcfromtimestamp(ts).date()


def _to_text(b):
    return (b.decode("utf-8", "ignore") if isinstance(b, bytes) else b).strip()


# below: 'commit' is provided by git-filter-repo at runtime
commit_date = _to_date(commit.committer_date)
msg = _to_text(commit.message)
author = _to_text(commit.author_name)

# 这里按你旧逻辑匹配：作者 github-actions[bot]，message 精确匹配 ci: auto-build，且早于 cutoff
if author == "github-actions[bot]" and msg == "ci: auto-build" and commit_date < cutoff:
    # 安全替代：不要 commit.skip()
    # 把这个提交变为空提交（清空文件变更），只清理该 commit 的内容，不影响后继提交樹结构
    commit.file_changes = []  # 清空改动
    # 也可以清空 message 或 author（可选），视需要而定：
    # commit.message = b"[removed auto-build]"
    # commit.author_name = b"removed"
