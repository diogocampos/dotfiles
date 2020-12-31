#!/usr/bin/env node

const IMAWA = '今は'
const REIJI = '零時'
const SHOUGO = '正午'
const GOZEN = '午前'
const GOGO = '午後'
const JI = '時'
const FUN = '分'
const HAN = '半'
const CHOUDO = 'ちょうど'
const GORO = 'ごろ'
const DESU = 'です。'

function main() {
  const phrase = generatePhrase(new Date())
  if (!process.stdout.isTTY) console.error(phrase)
  console.log(phrase)
}

function generatePhrase(date) {
  let hh = date.getHours()
  let mm = date.getMinutes()

  const imawa = coinFlip() ? IMAWA : ''

  const choudo = (mm === 0 || mm === 30) && coinFlip() ? CHOUDO : ''

  let goro = ''
  const rounded = coinFlip() && round(hh, mm)
  if (rounded && (rounded.hh !== hh || rounded.mm !== mm)) {
    ;({ hh, mm } = rounded)
    goro = GORO
  }

  let ampm = ''
  if (hh % 12 > 0 && coinFlip()) {
    ampm = hh < 12 ? GOZEN : GOGO
    hh %= 12
  }

  const hour
    = hh === 0 && mm === 0 ? REIJI
    : hh === 12 && mm === 0 ? SHOUGO
    : `${hh}${JI}`

  const minute
    = mm === 0 ? ''
    : mm === 30 && (goro || coinFlip()) ? HAN
    : `${mm}${FUN}`

  const hhmm = `${hour}${minute}`
  const time = ampm || coinFlip() ? `${hhmm}${choudo}` : `${choudo}${hhmm}`

  return `${imawa}${ampm}${time}${goro}${DESU}`
}

function round(hh, mm) {
  if (mm < 5) {
    mm = 0
  } else if ((25 < mm && mm < 30) || (30 < mm && mm < 35)) {
    mm = 30
  } else if (55 < mm) {
    hh = (hh + 1) % 24
    mm = 0
  }

  return { hh, mm }
}

function coinFlip() {
  return Math.random() > 0.5
}

main()
