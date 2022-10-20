import React from "react";
import spinner from "../../../assets/gifs/spinner.gif";

export function Spinner() {
  return (
    <div>
          <img
              src={spinner}
              style={{ width: "22px", height: "22px" }}
              alt="Loading..."
          />
    </div>
  );
};
