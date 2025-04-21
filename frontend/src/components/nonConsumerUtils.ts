// Типи даних
export type Payment = {
    amount: number;
    date: Date;
  };
  
  export enum TimePeriodType {
    DAY = 0,
    MONTH = 1,
    QUARTER = 2,
    YEAR = 3,
  }
  
  export type Rate = {
    value: number; // Наприклад, 0.01
    frequency: TimePeriodType;
  };
  
  export type TimePeriod = {
    unit: TimePeriodType;
    duration: number;
    startDate: Date;
  };
  
  // Обчислення тривалості між двома датами в одиницях (дні, місяці тощо)
  export function calcDuration(startDate: Date, endDate: Date, type: TimePeriodType): number {
    const diffTime = endDate.getTime() - startDate.getTime();
    switch (type) {
      case TimePeriodType.DAY:
        return Math.floor(diffTime / (1000 * 60 * 60 * 24));
      case TimePeriodType.MONTH:
        return (endDate.getFullYear() - startDate.getFullYear()) * 12 + endDate.getMonth() - startDate.getMonth();
      case TimePeriodType.QUARTER:
        return (
          (endDate.getFullYear() - startDate.getFullYear()) * 12 + endDate.getMonth() - startDate.getMonth()
        ) / 3;
      case TimePeriodType.YEAR:
        return endDate.getFullYear() - startDate.getFullYear();
    }
  }
  
  // Кінець періоду
  export function getEndDate(period: TimePeriod): Date {
    const date = new Date(period.startDate);
    switch (period.unit) {
      case TimePeriodType.DAY:
        date.setDate(date.getDate() + period.duration);
        break;
      case TimePeriodType.MONTH:
        date.setMonth(date.getMonth() + period.duration);
        break;
      case TimePeriodType.QUARTER:
        date.setMonth(date.getMonth() + period.duration * 3);
        break;
      case TimePeriodType.YEAR:
        date.setFullYear(date.getFullYear() + period.duration);
        break;
    }
    return date;
  }
  
  // Розрахунок останнього платежу
  export function calcLastPayment(
    amount: number,
    rate: Rate,
    repaymentPeriod: TimePeriod,
    payments: Payment[]
  ): Payment {
    let cumulativeAmount = amount;
    const startDate = repaymentPeriod.startDate;
    const endDate = getEndDate(repaymentPeriod);
  
    for (const payment of payments) {
      const duration = calcDuration(startDate, payment.date, rate.frequency);
      cumulativeAmount *= Math.pow(1 + rate.value, duration);
      cumulativeAmount -= payment.amount;
    }
  
    const finalDuration = calcDuration(startDate, endDate, rate.frequency);
    cumulativeAmount *= Math.pow(1 + rate.value, finalDuration);
  
    return {
      amount: cumulativeAmount,
      date: endDate,
    };
  }
  
  // Розрахунок прибутку
  export function computeIncome(
    amount: number,
    rate: Rate,
    repaymentPeriod: TimePeriod,
    payments: Payment[]
  ): number {
    let total = -amount;
    const startDate = repaymentPeriod.startDate;
    const endDate = getEndDate(repaymentPeriod);
  
    for (const payment of payments) {
      const duration = calcDuration(startDate, payment.date, rate.frequency);
      total += payment.amount / Math.pow(1 + rate.value, duration);
    }
  
    const lastPayment = calcLastPayment(amount, rate, repaymentPeriod, payments);
    const finalDuration = calcDuration(startDate, lastPayment.date, rate.frequency);
    total += lastPayment.amount / Math.pow(1 + rate.value, finalDuration);
  
    return total;
  }
  