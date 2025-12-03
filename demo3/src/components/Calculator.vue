<template>
  <div class="calculator">
    <div class="display">
      <div class="display-value" :class="{ 'small-text': displayValue.length > 9 }">
        {{ displayValue }}
      </div>
    </div>
    <div class="buttons">
      <div class="row">
        <button class="btn function" @click="clear">{{ clearText }}</button>
        <button class="btn function" @click="toggleSign">+/-</button>
        <button class="btn function" @click="percentage">%</button>
        <button class="btn operator" :class="{ active: currentOperator === '/' }" @click="setOperator('/')">÷</button>
      </div>
      <div class="row">
        <button class="btn number" @click="inputDigit('7')">7</button>
        <button class="btn number" @click="inputDigit('8')">8</button>
        <button class="btn number" @click="inputDigit('9')">9</button>
        <button class="btn operator" :class="{ active: currentOperator === '*' }" @click="setOperator('*')">×</button>
      </div>
      <div class="row">
        <button class="btn number" @click="inputDigit('4')">4</button>
        <button class="btn number" @click="inputDigit('5')">5</button>
        <button class="btn number" @click="inputDigit('6')">6</button>
        <button class="btn operator" :class="{ active: currentOperator === '-' }" @click="setOperator('-')">−</button>
      </div>
      <div class="row">
        <button class="btn number" @click="inputDigit('1')">1</button>
        <button class="btn number" @click="inputDigit('2')">2</button>
        <button class="btn number" @click="inputDigit('3')">3</button>
        <button class="btn operator" :class="{ active: currentOperator === '+' }" @click="setOperator('+')">+</button>
      </div>
      <div class="row">
        <button class="btn number zero" @click="inputDigit('0')">0</button>
        <button class="btn number" @click="inputDecimal">.</button>
        <button class="btn operator" @click="calculate">=</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const displayValue = ref('0')
const firstOperand = ref(null)
const currentOperator = ref(null)
const waitingForSecondOperand = ref(false)

const clearText = computed(() => {
  return displayValue.value === '0' && firstOperand.value === null ? 'AC' : 'C'
})

function inputDigit(digit) {
  if (waitingForSecondOperand.value) {
    displayValue.value = digit
    waitingForSecondOperand.value = false
  } else {
    displayValue.value = displayValue.value === '0' ? digit : displayValue.value + digit
  }
}

function inputDecimal() {
  if (waitingForSecondOperand.value) {
    displayValue.value = '0.'
    waitingForSecondOperand.value = false
    return
  }
  if (!displayValue.value.includes('.')) {
    displayValue.value += '.'
  }
}

function clear() {
  if (clearText.value === 'AC') {
    displayValue.value = '0'
    firstOperand.value = null
    currentOperator.value = null
    waitingForSecondOperand.value = false
  } else {
    displayValue.value = '0'
  }
}

function toggleSign() {
  const value = parseFloat(displayValue.value)
  displayValue.value = formatNumber(value * -1)
}

function percentage() {
  const value = parseFloat(displayValue.value)
  displayValue.value = formatNumber(value / 100)
}

function setOperator(operator) {
  const inputValue = parseFloat(displayValue.value)

  if (firstOperand.value === null) {
    firstOperand.value = inputValue
  } else if (currentOperator.value) {
    const result = performCalculation(firstOperand.value, inputValue, currentOperator.value)
    displayValue.value = formatNumber(result)
    firstOperand.value = result
  }

  waitingForSecondOperand.value = true
  currentOperator.value = operator
}

function calculate() {
  if (currentOperator.value === null || waitingForSecondOperand.value) {
    return
  }

  const inputValue = parseFloat(displayValue.value)
  const result = performCalculation(firstOperand.value, inputValue, currentOperator.value)

  displayValue.value = formatNumber(result)
  firstOperand.value = null
  currentOperator.value = null
  waitingForSecondOperand.value = false
}

function performCalculation(first, second, operator) {
  switch (operator) {
    case '+':
      return first + second
    case '-':
      return first - second
    case '*':
      return first * second
    case '/':
      return second !== 0 ? first / second : 'Error'
    default:
      return second
  }
}

function formatNumber(num) {
  if (num === 'Error') return 'Error'

  const str = num.toString()
  if (str.length > 12) {
    if (Math.abs(num) < 1e-6 || Math.abs(num) >= 1e9) {
      return num.toExponential(5)
    }
    return parseFloat(num.toPrecision(9)).toString()
  }
  return str
}
</script>

<style scoped>
.calculator {
  width: 100%;
  max-width: 375px;
  margin: 0 auto;
  background-color: #000;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0 12px 20px;
  box-sizing: border-box;
}

.display {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 20px 15px;
  min-height: 120px;
}

.display-value {
  color: #fff;
  font-size: 80px;
  font-weight: 300;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
  line-height: 1;
  text-align: right;
  word-break: break-all;
}

.display-value.small-text {
  font-size: 50px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.row {
  display: flex;
  gap: 12px;
}

.btn {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: none;
  font-size: 32px;
  font-weight: 400;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
  cursor: pointer;
  transition: opacity 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:active {
  opacity: 0.7;
}

.btn.number {
  background-color: #333;
  color: #fff;
}

.btn.function {
  background-color: #a5a5a5;
  color: #000;
}

.btn.operator {
  background-color: #ff9f0a;
  color: #fff;
}

.btn.operator.active {
  background-color: #fff;
  color: #ff9f0a;
}

.btn.zero {
  width: 172px;
  border-radius: 40px;
  justify-content: flex-start;
  padding-left: 32px;
}

/* Responsive sizing */
@media (max-width: 375px) {
  .btn {
    width: calc((100vw - 60px) / 4);
    height: calc((100vw - 60px) / 4);
  }

  .btn.zero {
    width: calc((100vw - 60px) / 2 + 12px);
  }

  .display-value {
    font-size: 60px;
  }

  .display-value.small-text {
    font-size: 40px;
  }
}
</style>
