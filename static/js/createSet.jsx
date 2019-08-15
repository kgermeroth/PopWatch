// Creates plus sign icon
class Add extends React.Component {
	render() {
		return (
			<i className="fas fa-plus"></i> 
			);
	}
}

// Creates trashcan icon
class Trash extends React.Component {
	render() {
		return (
			<i className="fas fa-trash"></i>
			);
	}
}

// this is the dropdown to select a hotel
class HotelNameSelector extends React.Component {
	constructor(props) {
		super(props);		
	}
	render() {
		console.log(this.props.hotels);
		return(<select>
			{ this.props.hotels.map((hotel) => {
				return (
				<option key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>
				)
			})}
			}
		</select>
			)
	}
}

// Test combining both elements (and see if icons render)
class HotelContainer extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			hotels:[]
		}
	}

	//when this component mounts, change the state to be 
	componentDidMount() {
		const hotels = [{hotel_id: 1, hotel_name: "Grand Hyatt"}];
		this.setState ({
			hotels
		});
	}
	render() {
		return (<div>
			<HotelNameSelector hotels={this.state.hotels}/>
			<Trash />
			</div>
		);
	}
}

ReactDOM.render(
	React.createElement(HotelContainer, null),
	document.getElementById("hotel-dropdowns")
	);

