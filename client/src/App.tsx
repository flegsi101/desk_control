import React, { useEffect, useState } from "react"
import "./App.scss"
import { HexColorPicker } from "react-colorful"
import axios from "axios"
import socketIOClient, { Socket } from "socket.io-client"
import Toggle from "./components/Toggle"

const api = axios.create({
  baseURL: "http://192.168.178.5:5000/desk_control/api",
})

const SOCKET = "http://192.168.178.5:5000"
const socket = socketIOClient(SOCKET)

function App() {
  const [color, setColor] = useState<string>()

  useEffect(() => {
    socket.on("color", (color) => {
      setColor(color)
    })
  })

  const changeColor = (color: string) => {
    socket.emit("color", color)
    setColor(color)
  }

  useEffect(() => {
    if (!color) {
      api.get("/state").then((res) => {
        if (res.status == 200) {
          setColor(res.data.color)
        }
      })
    }
  })

  return (
    <div className="app">
      <div className="control led-toggle">
        <p>Toggle led</p>
        <Toggle></Toggle>
      </div>
      <div className="control led-toggle">
        <div className="label">
          <p>Select color</p>
        </div>
        <div className="led-color--preview">
          <p>Selected: {color}</p>
          <div style={{ background: color }}></div>
        </div>
        <HexColorPicker color={color} onChange={changeColor} />
      </div>
    </div>
  )
}

export default App
