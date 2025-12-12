# 检查是否提供了 Version
if [ -z "$1" ]; then
  echo "Missing Version! Please provide a version number like 0.1.7"
  exit 1
fi


if [ -z "$2" ]; then
  echo "Missing Commit Message! Please provide a commit message like 'Update version'"
  exit 1
fi

VERSION=$1

TAG_MESSAGE="Publish version v$VERSION"
COMMIT_MESSAGE=$2

# 检测操作系统类型并使用正确的 sed 命令
echo "[Updating version in pyproject.toml...]"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS 版本
    sed -i '' "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
else
    # Linux 版本
    sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
fi


# 提交到 git
echo "[Committing to git...]"
git add .
git commit -m "$COMMIT_MESSAGE"
git push

# add tag
echo "[Adding tag...]"
git tag -a "v$VERSION" -m "$TAG_MESSAGE"
git push origin "v$VERSION"

echo "[Done!] The version $VERSION has been published to TestPyPI."