import { open } from 'lmdb'
import { $, fs, os } from 'zx'
import { generatePassword, mkdirp } from './utils'
import { isFreePort } from 'find-free-ports'
import { spinner } from '@clack/prompts'
import { cp, cpSync } from 'fs'
import { makeDai } from './web3'

export type BEE = {
  beeId: number
  processName: string
  port: number
  configFile: string
  command: string
  mode: BEE_MODE
}

let DB: any

export const BEEST = `████████╗ ███████╗███████╗███████╗████████╗
│  ██╔════██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
│  ████████╔╝█████╗  █████╗  ███████╗   ██║   
│  ██╔════██╗██╔══╝  ██╔══╝  ╚════██║   ██║   
│  ████████╔╝███████╗███████╗███████║   ██║   
│  ╚═══════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝   v0.0.1
│  Bees Toolkit for Swarm`

export const GOODBYE = `Happy Swarming 🐝🐝🐝`

export const HOME_DIR = os.homedir()
export const BEEST_DIR = `${HOME_DIR}/.beest`
export const BEES_DIR = `${BEEST_DIR}/bees`
export const BIN_DIR = `${BEEST_DIR}/bin`
export const BEE_CMD = `${BIN_DIR}/bee`
export const GNOSIS_RPC_DEFAULT = 'https://rpc.gnosis.gateway.fm'

export enum KEY {
  'NEXT_PORT',
  'FUNDING_WALLET',
  'GNOSIS_RPC',
  'FUNDING_WALLET_PK',
  'BEES',
  'ETHERPROXY',
}

export enum BEE_MODE {
  ULTRALIGHT = 'ultralight',
  LIGHTNODE = 'light',
  FULLNODE = 'full',
}

export const ETHERPROXY_PORT = 9999
export const ETHERPROXY_URL = `http://localhost:${ETHERPROXY_PORT}`
export const BEEST_PASSWORD_FILE = `${BEEST_DIR}/beest.pwd`

export async function initBeest() {
  // if(!fs.existsSync(BEEST_DIR)){
  // await $`mkdir -p ${BEEST_DIR}`
  mkdirp(BEEST_DIR)
  // }
  // if(!fs.existsSync(BEES_DIR)){
  //     await $`mkdir -p ${BEES_DIR}`
  mkdirp(BEES_DIR)
  // }
  // if(!fs.existsSync(BIN_DIR)){
  //     await $`mkdir -p ${BIN_DIR}`
  mkdirp(BIN_DIR)
  // }
  let pwdFile = BEEST_PASSWORD_FILE
  if (!fs.existsSync(pwdFile)) {
    fs.writeFileSync(pwdFile, generatePassword())
  }
  return beestDb()
}

export async function installBee() {
  if (!fs.existsSync(`${BIN_DIR}/bee`)) {
    const s = spinner()
    s.start(`Installing latest bee version into ${BEE_CMD}`)
    let out = (await $`wget -q -O - https://raw.githubusercontent.com/ethersphere/bee/master/install.sh`).stdout
    out = out.replace('/usr/local/bin', BIN_DIR).replace('USE_SUDO:="true"', 'USE_SUDO:="false"')
    fs.writeFileSync(`${BIN_DIR}/install.sh`, out)
    // console.log(`/usr/bin/bash ${BIN_DIR}/install.sh`)
    out = (await $`/usr/bin/bash ${BIN_DIR}/install.sh`).stdout
    // console.log(out)
    s.stop(`Installed bee into ${BEE_CMD}`)
    const beeVersion = (await $`${BEE_CMD} version`).stdout.trim()
    // console.log({beeVersion})
    cpSync(BEE_CMD, `${BEE_CMD}-${beeVersion}`)
  }
}

export const beestDb = () => {
  if (!DB) {
    DB = open({
      path: `${HOME_DIR}/.beest/beest.lmdb`,
      compression: true,
    })
  }
  return DB
}

export const getConfig = <T>(key: KEY, val: T): T => {
  let res = beestDb().get(key)
  return res || val
}

export const putConfig = (key: KEY, val: any) => {
  if (key == KEY.GNOSIS_RPC && val.trim() == '') {
    return
  }
  beestDb().putSync(key, val)
}

export const pushConfig = (key: KEY, newItem: any) => {
  let value = getConfig(key, [])
  value.push(newItem)
  beestDb().putSync(key, value)
}

export const newBeeId = () => {
  let i = 1
  while (true) {
    if (!fs.existsSync(beeDataDir(i))) {
      return i
    } else {
      i++
    }
  }
}

export const beeDataDir = (beeId: number) => {
  const number = padBeeId(beeId)
  const datadir = `bee${number}`
  return `${BEES_DIR}/${datadir}`
}

export const padBeeId = (beeId: number) => {
  return beeId.toString().padStart(3, '0')
}

export const freeBeePorts = async () => {
  // console.log('KEY.NEXT_PORT',getConfig(KEY.NEXT_PORT))
  let ports = []
  let i = nextFreePort() || 1633
  while (true) {
    // console.log({i})
    const free = await isFreePort(i)
    // const free = await portUsed.check(i,'127.0.0.1')
    // console.log({i,free})
    if (free) {
      ports.push(i)
      if (ports.length == 2) {
        // beestDb().putSync('NEXT_PORT',i+1)
        putConfig(KEY.NEXT_PORT, i + 1)
        return ports
      } else {
        i++
      }
    } else {
      i++
    }
  }
}

export const nextFreePort = () => {
  if (fs.readdirSync(BEES_DIR).length === 0) {
    putConfig(KEY.NEXT_PORT, 1633)
    return 1633
  }
  return getConfig(KEY.NEXT_PORT, 0)
}