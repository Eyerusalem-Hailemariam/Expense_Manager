<script setup>
import { AxisChart } from "frappe-ui"


const chartConfig = {
    data: [
        { month: 'Jan', expenses: 200 },
        { month: 'Feb', expenses: 300 },
        { month: 'Mar', expenses: 250 },
        { month: 'Apr', expenses: 350 },
        { month: 'May', expenses: 400 },
        { month: 'Jun', expenses: 300 },
    ],
    title: 'Monthly Expense',
    xAxis: { key: 'month', title: 'Month' },
    yAxis: { title: 'Amount ($)', echartOptions: { min: 0, max: 500},
    series: [{ name: 'sales', type: 'bar' }]
    }
}
</script>
<template>
    <div>
  <AxisChart
    :config="chartConfig" />
  />
  </div>
</template>
