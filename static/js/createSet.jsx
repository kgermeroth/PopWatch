// This component is the add sign
class Add extends React.Component {
	constructor() {
		super();
		this.addHotel = this.addHotel.bind(this);
	}

	// This function will create a new HotelContainer, but is executed in HotelDropDowns
	addHotel() {
		this.props.onClick()
	}

	render() {
		return (
			<p>Add Hotel: <i 
			onClick={this.addHotel} 
			className="fas fa-plus"
			></i></p> 
			);
	}
}

// This component is the trash icon
class Trash extends React.Component {
	constructor() {
		super();
	}

	render() {
		return (
			<i onClick={this.props.handleOnClick} className="fas fa-trash"></i>
			);
	}
}

// this is the dropdown to select a hotel
class HotelNameSelector extends React.Component {
	constructor() {
		super();
	}		 
	
	render() {
		// create an empty list
		const hotel_options = [];

		//adds the default "Select Hotel" to the hotel_options list
		hotel_options.push(<option key="0" defaultValue>Select Hotel</option>)

		// Loop through each hotel in the hotels property (JSON object), and append an option tag with the hotel variables inside
		// the list of hotels comes from the property on the HotelContainer class which comes from the state on the HotelDropDowns when the component mounts
		for (const hotel of this.props.hotels) {
			hotel_options.push(<option key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>);
		}

		// return the array of options in select tags
		return (
			<select
				name="hotel_choice[]"	
				onChange={this.props.handleChange}
				value={this.props.value}
			>
				{hotel_options}
			</select>
		);
			
	}
}

// This component holds the HotelNameSelector (hotel dropdown) and the trash icon
class SingleHotelContainer extends React.Component {
	constructor() {
		super();
	}
	// write handleChange function with event to get hotel_id

	render() {
		return (<div className="HotelContainer">
			<HotelNameSelector
				hotels={this.props.hotels}
				handleChange={this.props.handleChange}
				value={this.props.selectedHotel}
			/>
			<Trash handleOnClick={this.props.handleDropContainer} />
			</div>
		);
	}
}

// This component holds everything: multiple HotelContainers (which are the hotel dropdown and trash icon) and the addHotel icon
class AllHotelDropDowns extends React.Component {

    constructor() {
    	super();
        this.state = {
            hotels: [],
            hotelContainers: [
            	{ selectedHotel: 'Select Hotel' }			
            ]
        };
        this.addHotel = this.addHotel.bind(this);
        this.dropHotelContainer = this.dropHotelContainer.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
	// AJAX request to get a list of hotels from db
		const hotels = $.get('/hotels.json', (hotels)=> this.setState({
			hotels
		}));
    }

    handleChange(idx, event) {
    	const newHotelContainers = this.state.hotelContainers.slice();
    	const value = event.target.value;

    	newHotelContainers[idx] = { selectedHotel: value };

    	this.setState({ hotelContainers: newHotelContainers });

    	// need to remove this hotel from the availhotels state as well!
    }

    addHotel() {
    	
    	const hotelContainers = this.state.hotelContainers;

    	if (hotelContainers.length < 8) {
	    	// add a new hotel container to the list, this will create a new hotel container
	    	hotelContainers.push({ selectedHotel: 'Select Hotel' });
	    	 // update the react state
    		this.setState({ hotelContainers });
	    } else {
	    	alert('There is a maximum of 8 hotels.');
	    }



    }

    dropHotelContainer(idx) {

    	const newHotelContainers = this.state.hotelContainers.slice();
		newHotelContainers.splice(idx, 1);

    	this.setState({hotelContainers: newHotelContainers});
    }

    render() {

        const hotelContainers = this.state.hotelContainers.map((hotelContainer, idx) => {
            return (
            	<SingleHotelContainer
                	key={idx}
                	handleDropContainer={() => this.dropHotelContainer(idx)}
                	handleChange={(event) => this.handleChange(idx, event)} 
                	hotels={this.state.hotels}
                	selectedHotel={hotelContainer.selectedHotel}
            	/>
            );
        });

        return (
            <div>
                <div className="selected-hotels">
                    {hotelContainers}
                </div>

                <Add onClick={this.addHotel}/>
           </div> 
        );
	};
}

ReactDOM.render(
	<AllHotelDropDowns />,
	document.getElementById("hotel-dropdowns")
	);