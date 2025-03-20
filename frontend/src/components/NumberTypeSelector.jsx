import { useContext } from 'react';
import { NumbersContext } from '../contexts/NumbersContext';

const NumberTypeSelector = () => {
  const { numberType, setNumberType } = useContext(NumbersContext);

  return (
    <div className="type-selector">
      <select 
        value={numberType} 
        onChange={(e) => setNumberType(e.target.value)}
      >
        <option value="primes">Prime Numbers</option>
        <option value="fibo">Fibonacci Numbers</option>
        <option value="even">Even Numbers</option>
        <option value="rand">Random Numbers</option>
      </select>
    </div>
  );
};

export default NumberTypeSelector;
