import { createContext, useState, useEffect } from 'react';

export const NumbersContext = createContext();

export const NumbersProvider = ({ children }) => {
  const [windowSize] = useState(10);
  const [numbers, setNumbers] = useState([]);
  const [avg, setAvg] = useState(0);
  const [numberType, setNumberType] = useState('primes');

  const updateWindow = (newNumbers) => {
    setNumbers(prev => {
      const combined = [...prev, ...newNumbers];
      const unique = [...new Set(combined)];
      return unique.slice(-windowSize);
    });
  };

  useEffect(() => {
    const calculateAvg = () => {
      const sum = numbers.reduce((a, b) => a + b, 0);
      setAvg(sum / numbers.length || 0);
    };
    calculateAvg();
  }, [numbers]);

  return (
    <NumbersContext.Provider value={{ numbers, avg, numberType, setNumberType, updateWindow }}>
      {children}
    </NumbersContext.Provider>
  );
};
