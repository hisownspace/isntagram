import React, { useEffect, useState } from "react";

const PatternForm = () => {
  
  const  [zipCode, setZipCode] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  // const changePhone = (e) => {
  //   const reArea = /^\( \d{3}$/;
  //   const areaFirst = /^\d{1}$/;
  //   const areaPartial1 = /^\( \d{1}$/;
  //   const areaPartial2 = /^\( \d{2}$/;
  //   const fullArea = /^\(\d{3} $/
  //   const delArea = /^\( \d{3} \)$/;
  //   const emptyArea = /^\( $/;
  //   const firstTrip = /\( \d{3} \) \d{3}$/;
  //   const finalNumber = /\( \d{3} \) \d{3} - \d{5}/;
  //   const correctNum = /^\( \d{3} \) \d{0,3}? ?-? ?\d{0,4}?/;
  //   const charCheck = /^[ \(\)\d\-]*$/
  //   const deleteBlock = /^\( \d{3} \) \d{3} -$/

  //   if (!charCheck.test(e.target.value)) {
  //     return;
  //   }

  //   if (delArea.test(e.target.value)) {
  //     console.log("deleting area code")
  //     setPhoneNumber(e.target.value.slice(0,4))
  //   } else if (areaFirst.test(e.target.value)) {
  //     console.log("in area first block");
  //     setPhoneNumber("( " + e.target.value);
  //   } else if (areaPartial2.test(e.target.value) || e.target.value === "") {
  //     console.log("in areaPartial block");
  //     setPhoneNumber(e.target.value);
  //   } else if (emptyArea.test(e.target.value)) {
  //     setPhoneNumber("");
  //   } else if (areaPartial1.test(e.target.value )) {
  //     setPhoneNumber(e.target.value);
  //   };

  //   if (reArea.test(e.target.value)) {
  //     console.log("in reArea block");
  //     setPhoneNumber(e.target.value + " ) ");
  //   } 
  //   else if (fullArea.test(e.target.value)) {
  //     setPhoneNumber(e.target.value);
  //   };

  //   if (firstTrip.test(e.target.value)) {
  //     setPhoneNumber(e.target.value + " - ");
  //   } else if (finalNumber.test(e.target.value)) {
  //     setPhoneNumber(e.target.value.slice(0,18));
  //   } else if (correctNum.test(e.target.value)) {
  //     setPhoneNumber(e.target.value)
  //   };
  //   if (deleteBlock.test(e.target.value)) {
  //     setPhoneNumber(e.target.value.slice(0, 10));
  //   };
  // };

  const returnDigits = (phoneNum) => {
    return phoneNum.replace(/[^\d]/g, '');
  };

  const changePhone = e => {
    const num = e.target.value;

    const justNums = returnDigits(num);

    if (justNums.length === 0) {
      setPhoneNumber("");
    } else if (justNums.length <= 3) {
      setPhoneNumber("( " + justNums);
    } else if (justNums.length <= 6) {
      setPhoneNumber("( " + justNums.slice(0,3) + " ) " + justNums.slice(3,6));
    } else if (justNums.length <= 10) {
      setPhoneNumber("( " + justNums.slice(0,3) + " ) " + justNums.slice(3,6) + "-" + justNums.slice(6));
    };

  };

  const changeZip = (e) => {
    const zipRe = /^\d{0,5}$/;

    const match = zipRe.test(e.target.value);

    if (match) {
      setZipCode(e.target.value);
    };
  };

  return (
    <div>
      <form>
        <input
          pattern="\d{5}"
          value={zipCode}
          onChange={changeZip}
        >
        </input>
        <input
          pattern="\(\d{3}) \d{3}-\d{4}"
          placeholder={phoneNumber}
          onChange={changePhone}
          value={phoneNumber}
          >
          </input>
        <button
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default PatternForm;