# CI-CD-Test

## git commit格式

**规范格式：**

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

对于大部分提交，我们只需要关心第一行 `header` 部分：`<type>(<scope>): <subject>`。

- **`type` (类型)**：必填，说明这次提交的性质。常用的 `type` 包括：
	- `feat`: 新功能 (feature)
	- `fix`: 修复 bug
	- `docs`: 只修改了文档 (documentation)
	- `style`: 代码格式修改，不影响代码逻辑 (空格、格式化、缺少分号等)
	- `refactor`: 代码重构，既不是修复 bug 也不是新增功能
	- `test`: 增加或修改测试
	- `chore`: 构建过程或辅助工具的变动 (比如修改 CI 流程)
	- `ci`: 对 CI 配置或脚本的修改
- **`scope` (范围)**：选填，说明本次提交影响的范围。例如 `(api)`, `(db)`, `(calc)`。
- **`subject` (主题)**：必填，简短描述本次提交的目的，不超过 50 个字符。
	- 以动词开头，使用第一人称现在时，比如 `change` 而不是 `changed` 或 `changes`。
	- 第一个字母小写。
	- 末尾不加句号 (`.`)。

**示例：**

- **好的示例**:

	```
	feat(parser): add support for parentheses
	fix: correct calculation for division by zero
	docs: update README with setup instructions
	chore: upgrade pytest to version 8.5.0
	```

- **不好的示例**:

	```
	fixed the bug
	Update
	WIP
	```



#### 1. `name`

```
name: Node.js CI/CD Pipeline
```

- **作用**：定义工作流的名称。这个名字会显示在你的 GitHub 仓库的 "Actions" 标签页中，方便识别。

#### 2. `on`

```
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
```

- **作用**：定义触发工作流的事件。
- `push`: 当有代码被推送到指定分支时触发。这里我们指定了 `main` 分支。
- `pull_request`: 当有人创建一个指向 `main` 分支的 Pull Request 或更新该 PR 时触发。这对于在合并代码前进行检查非常重要。

#### 3. `permissions`

```
permissions:
  contents: read
  packages: write
  pages: write
  id-token: write
```

- **作用**：设置 `GITHUB_TOKEN` 的权限范围，遵循最小权限原则，提高安全性。
- `contents: read`: 允许 `actions/checkout` 拉取代码。
- `packages: write`: 允许向 GitHub Container Registry 推送 Docker 镜像。
- `pages: write` 和 `id-token: write`: 部署到 GitHub Pages 所需的权限。

#### 4. `jobs`

工作流由一个或多个 `job`（任务）组成。默认情况下，所有 `job` 并行运行，但我们可以通过 `needs` 关键字定义依赖关系。

##### 4.1 `build-and-test` Job

这是CI阶段的核心任务。

- `runs-on: ubuntu-latest`：指定任务运行在 GitHub 托管的最新版 Ubuntu 虚拟机上。
- `steps`：定义该任务按顺序执行的步骤。
  - `uses: actions/checkout@v4`：这是一个官方的 Action，作用是**检出你的仓库代码**到虚拟机中，以便后续步骤可以访问它。
  - `uses: actions/setup-node@v4`：设置指定的 Node.js 环境。`with: cache: 'npm'` 会缓存依赖，如果 `package-lock.json` 没有变化，下次运行时会快很多。
  - `run: npm ci`：执行 shell 命令。`npm ci` 会根据 `package-lock.json` 文件精确安装依赖，比 `npm install` 更适合 CI 环境。
  - `run: npm run build` 和 `run: npm test`：执行你在 `package.json` 中定义的构建和测试脚本。
  - `uses: actions/upload-artifact@v4`：**将文件或目录打包成一个 "产物" (artifact)**。产物可以在不同的 `job` 之间共享。这里我们将构建结果上传，以便 `deploy-to-pages` 任务可以使用它。

##### 4.2 `build-and-push-docker` Job

这是CD阶段的一部分，负责容器化。

- `needs: build-and-test`：**关键！** 这表示此任务必须等待 `build-and-test` 任务成功完成后才能开始。
- `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`：**关键！** 这是一个条件判断。它确保这个部署任务**只在代码被直接推送到 `main` 分支时运行**，而不会在 Pull Request 中运行。
- `docker/login-action@v3`：登录到容器镜像仓库。这里我们使用 `ghcr.io`（GitHub 自己的镜像仓库），并使用自动生成的 `secrets.GITHUB_TOKEN` 进行身份验证。
- `docker/metadata-action@v5`：智能地为你的 Docker 镜像生成标签。例如，基于 Git 标签、分支名或 commit SHA。
- `docker/build-push-action@v5`：构建 Dockerfile 并将其推送到指定的仓库。

##### 4.3 `deploy-to-pages` Job

这是CD阶段的另一部分，负责部署到静态网站托管。

- `needs` 和 `if` 的作用同上，确保在正确的时间和条件下执行。
- `actions/download-artifact@v4`：下载之前 `build-and-test` 任务上传的产物。
- `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`：这是部署到 GitHub Pages 的标准三步曲。它们会配置环境，将你的文件打包成 Pages 接受的格式，然后完成部署。

------

1. **提交代码**：将上述所有文件提交到你的 GitHub 仓库。
2. **启用 GitHub Pages**：
   - 进入你的仓库 -> `Settings` -> `Pages`。
   - 在 `Build and deployment` 下的 `Source` 选择 `GitHub Actions`。
3. **触发 CI**：
   - 创建一个新的分支，做一些修改，然后创建一个 Pull Request 指向 `main` 分支。
   - 进入仓库的 `Actions` 标签页，你会看到 `build-and-test` 任务正在运行。但部署任务会因为 `if` 条件而被跳过。
4. **触发 CD**：
   - 将你的 Pull Request 合并到 `main` 分支。
   - 再次进入 `Actions` 标签页，你会看到工作流被再次触发。这次，在 `build-and-test` 成功后，`build-and-push-docker` 和 `deploy-to-pages` 任务也会被执行。
5. **验证结果**：
   - **Docker 镜像**：在你的个人主页或组织主页的 `Packages` 标签页中，可以看到新推送的容器镜像。
   - **GitHub Pages**：稍等片刻，访问你的 GitHub Pages URL (通常是 `https://<你的用户名>.github.io/<仓库名>/`)，应该能看到部署的内容。