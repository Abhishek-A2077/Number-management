import { useContext } from 'react';
import { NumbersContext } from '../contexts/NumbersContext';

const NumberWindow = () => {
  const { numbers } = useContext(NumbersContext);

  return (
    <div className="number-grid">
      {numbers.map((num, index) => (
        <div key={index} className="number-card">
          <span className="value">{num}</span>
          <span className="index">#{index + 1}</span>
        </div>
      ))}
    </div>
  );
};
