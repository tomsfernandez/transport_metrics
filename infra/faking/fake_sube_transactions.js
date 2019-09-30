const faker = require('faker');
const fs = require('fs');
const MAX_TRANSACTIONS_AMOUNT=6;
const tickets = { NORMAL: 10, ATRIBUTO_SOCIAL: 2.45, OTRO: 4.3 }
const stopped_stops = JSON.parse(fs.readFileSync(__dirname + '/stopped_stops.json'));

const generateRow = (timestamp, ticket_type, amount, vehicle_id) => {
  return {timestamp: timestamp,ticket_type: ticket_type, amount: amount,vehicle_id: vehicle_id}
}

const getTicketType = () => {
  const probability = Math.random();
  if (probability < 0.65) return "NORMAL";
  else if (probability < 0.9) return "ATRIBUTO_SOCIAL";
  else return "OTRO"; 
}

let result = []
let amount = 0
stopped_stops.forEach(stop => {
  if (amount % 100 === 0 ) console.log(`Created ${amount} rows...`)
  const amount_of_tickets = Math.round(MAX_TRANSACTIONS_AMOUNT * Math.random())
  const generated_tickets = [...Array(amount_of_tickets).keys()].map(x => getTicketType()).map(x => {
    return generateRow(stop.timestamp, x, tickets[x], stop.vehicle_id);
  });
  amount = amount + amount_of_tickets;
  result = result.concat(generated_tickets);
});
const data = JSON.stringify(result);
fs.writeFileSync('sube_transactions.json', data);