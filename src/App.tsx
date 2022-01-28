import React, { useEffect, useState } from "react"
import "./App.scss"
import { HexColorPicker } from "react-colorful"
import socketIOClient from "socket.io-client"
import Toggle, { ToggleState } from "./components/Toggle"

class LedState {
  constructor(public state: ToggleState = ToggleState.OFF, public color: string = "#ffffff") {}
}

const SOCKET = "http://192.168.178.29:5000"
const socket = socketIOClient(SOCKET)

function App() {
  const [color, setColor] = useState<string>()
  const [state, setState] = useState<ToggleState>()

  const updateState = (state: ToggleState) => {
    socket.emit("state", new LedState(state, color))
    setState(state)
  }

  const updateColor = (color: string) => {
    socket.emit("state", new LedState(ToggleState.ON, color))
    setColor(color)
  }

  useEffect(() => {
    socket.on("state", (state) => {
      setState(state.state)
      setColor(state.color)
    })
  }, [])

  return (
    <div className="app">
      <div className="app--header">
        <div className="app--header--title">Desk Control</div>
      </div>

      <div className="app--body">
        <p className="label">Toggle led</p>
        <Toggle state={state} onChange={updateState}></Toggle>

        <p className="label">Select color</p>
        <div className="led-color--preview">
          <p>{color}</p>
          <div style={{ background: color }}></div>
        </div>

        <div className="picker">
          <HexColorPicker color={color} onChange={updateColor} />
        </div>
      </div>
    </div>
  )
}

export default App
