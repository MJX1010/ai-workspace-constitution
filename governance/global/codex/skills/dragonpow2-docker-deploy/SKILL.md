---
name: dragonpow2-docker-deploy
description: Use when rebuilding, deploying, or debugging the DragonPow2 server Docker image, including xgame/xmongo remote Go module access, missing generated dg2/pb or dg2/res artifacts, Dockerfile runtime failures, and final image verification.
---

# DragonPow2 Docker Deploy

## Scope

Use this for `D:\Projects\DragonPow2\DragonPow2_Trunk_Leaning\server` when the goal is to rebuild or verify the `dg2-server:latest` Docker image.

The server module is `server\dg2`. The Dockerfile is `server\manifest\docker\Dockerfile`, and the build context is `server\dg2`.

## Workflow

1. Start from the server root:

```powershell
Set-Location D:\Projects\DragonPow2\DragonPow2_Trunk_Leaning\server
```

2. Check remote Go module access from `dg2` before blaming Docker:

```powershell
Set-Location .\dg2
$oldCache = $env:GOMODCACHE
$tmpCache = Join-Path $env:TEMP ("gomodcache-" + [guid]::NewGuid())
$env:GOMODCACHE = $tmpCache
go mod download -json xgame xmongo
$env:GOMODCACHE = $oldCache
Remove-Item -LiteralPath $tmpCache -Recurse -Force -ErrorAction SilentlyContinue
```

3. Verify generated artifacts exist. Current Docker builds need:

- `dg2\pb\datap`, `dg2\pb\csp`, `dg2\pb\ssp`, `dg2\pb\osp`, `dg2\pb\res`
- `dg2\pb\datap\init.gen.go`
- `dg2\pb\csp\cmd_registry.gen.go`
- `dg2\pb\csp\errors.gen.go` and `dg2\pb\ssp\errors.gen.go`
- `dg2\res\tables.gen.go`
- `dg2\server\gamesvr\module\cslog\cslog.go`

Official path: run the meta generator from `server\meta` when `hatch`, `pymodel`, and `protoc` access are available. If `pymodel` cannot be cloned from `gitlab.xg.bytedance.net/fanglijian/pymodel.git`, use the local proto fallback under `dg2\pb` and regenerate Go pb files with:

```powershell
Set-Location D:\Projects\DragonPow2\DragonPow2_Trunk_Leaning\server
$protoc = 'C:\Users\Admin\.nuget\packages\google.protobuf.tools\3.25.3\tools\windows_x64\protoc.exe'
$env:PATH = "C:\Users\Admin\go\bin;$env:PATH"
& $protoc -I . --go_out=. --go_opt=paths=source_relative `
  dg2/pb/datap/datap.proto `
  dg2/pb/res/res.proto `
  dg2/pb/csp/csp.proto `
  dg2/pb/ssp/ssp.proto `
  dg2/pb/osp/osp.proto
```

4. Run local compile and focused tests:

```powershell
Set-Location D:\Projects\DragonPow2\DragonPow2_Trunk_Leaning\server\dg2
go test ./res ./pkg/rewardkit ./pkg/roledirty ./server/gamesvr/module/reward
go build -o $env:TEMP\dg2-server-check.exe ./cmd/main.go
Remove-Item -LiteralPath $env:TEMP\dg2-server-check.exe -Force -ErrorAction SilentlyContinue
```

5. Rebuild the Docker image from the server root:

```powershell
Set-Location D:\Projects\DragonPow2\DragonPow2_Trunk_Leaning\server
$buildDate = (Get-Date).ToUniversalTime().ToString('yyyyMMddHHmmss')
$commit = (svn info --show-item revision 2>$null); if (-not $commit) { $commit = 'unknown' }
$branch = (Split-Path -Leaf (Resolve-Path .).Path); if (-not $branch) { $branch = 'unknown' }
docker build `
  --build-arg BUILD_VERSION=0.1.0 `
  --build-arg BUILD_COMMIT=$commit `
  --build-arg BUILD_BRANCH=$branch `
  --build-arg BUILD_DATE=$buildDate `
  -f manifest/docker/Dockerfile `
  -t dg2-server:latest `
  dg2/
```

6. Verify the image before claiming success:

```powershell
docker image inspect dg2-server:latest --format '{{.Id}} {{.Size}} {{json .Config.Entrypoint}}'
docker run --rm dg2-server:latest --help
```

## Known Failure Modes

- `go.mod` requires Go `1.25.5`; use `golang:1.25.5` or newer compatible tags.
- Alpine Go builder images can lack `git`, and `apk add git` may fail behind TLS/proxy issues. The working Dockerfile uses Debian-based `golang:1.25.5`.
- If the runtime stage is Alpine, set `CGO_ENABLED=0` in the builder. Otherwise the container can fail with `exec /app/server: no such file or directory` because the binary expects glibc.
- Do not force local `/deps/xgame` or `/deps/xmongo` replaces for this deployment path. The current `go.mod` remote replaces are `gitlab.xg.bytedance.net/fanglijian/xmongo v0.2.0` and `gitlab.xg.bytedance.net/fanglijian/xgame v0.1.0`.
- Missing `dg2/pb/...`, `dg2/res/tables.gen.go`, or `cslog` means generated artifacts are absent, not that `xgame/xmongo` failed.

## Completion Rule

Do not report the deployment as successful unless `go build`, `docker build`, `docker image inspect`, and `docker run --rm dg2-server:latest --help` have all run freshly in the current turn.
