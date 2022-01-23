import React, { useState } from "react"
import "./App.scss"
import { Color, ColorChangeHandler, HuePicker } from "react-color"
import axios from "axios"

const api = axios.create({
  baseURL: "http://192.168.178.5/desk_control/api",
})

function App() {
  const [color, setColor] = useState<Color>()

  return (
    <div className="App">
      <HuePicker color={color} onChange={(color) => setColor(color.hex)} />
      <p>{color}</p>
    </div>
  )
}

export default App
