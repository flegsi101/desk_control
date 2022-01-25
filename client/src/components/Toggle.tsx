import React, { useEffect, useState } from "react"
import "./Toggle.scss"

export enum ToggleState {
  OFF = 0,
  ON = 1,
}

interface ToggleProps {
  state?: ToggleState
  onChange?: (state: ToggleState) => void
}

const default_props: ToggleProps = {
  state: ToggleState.OFF,
}

function Toggle(props: ToggleProps = default_props) {
  const [_state, _setState] = useState(props.state)

  const updateState = () => {
    const newState = _state === ToggleState.ON ? ToggleState.OFF : ToggleState.ON
    _setState(newState)
    if (props.onChange) {
      props.onChange(newState)
    }
  }

  useEffect(() => {
    _setState(props.state)
  }, [props])

  return (
    <div
      className={`toggle ${_state === ToggleState.ON ? "on" : "off"}`}
      onClick={updateState}
    ></div>
  )
}

export default Toggle
