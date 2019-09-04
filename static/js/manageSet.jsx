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
			<p><b>Add Hotel: </b><i 
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
			// See if hotel is in the selected hotels list. If it's not then add to the dropdowns.
			// Also checks to see if the value matches the hotel id, will display the name for the dropdown it is
			// selected for, but not the others (because the value is specific to dropdown on which it was selected)
			if ((!(this.props.selectedHotels.includes(hotel.hotel_id))) || this.props.value === hotel.hotel_id) {
				hotel_options.push(<option key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>);
			}
		}

		// return the array of options in select tags
		return (
			<select
				className="hotel_dropdown"
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

	render() {
		return (<div className="HotelContainer">
			<HotelNameSelector
				hotels={this.props.hotels}
				handleChange={this.props.handleChange}
				value={this.props.selectedHotel}
				selectedHotels={this.props.selectedHotels}
			/>
			<Trash handleOnClick={this.props.handleDropContainer} />
			</div>
		);
	}
}

// This component is the dropdown that lists all the comp sets
class CompSetDropdown extends React.Component {
	constructor () {
		super();
	}

	render() {

		const comp_sets = [];

		for (const set of this.props.compSetIDAndName) {
			comp_sets.push(<option key={set.view_id} value={set.view_id} defaultValue={this.props.currentSetChoice === set.view_id}>{set.view_name}</option>);
		}

		return (
			<select
				className="comp_set_dropdown"
				name="comp_sets"
				onChange={this.props.onChange}
				>{ comp_sets }</select>)
	}
}

class CompSetName extends React.Component {
	constructor () {
		super();
	}

	render() {

		return (
			<input type="text" name="set_name" id="set_name" defaultValue={this.props.currentSetName} onChange={this.props.onChange}></input>
			)
	}
}

class Default extends React.Component {
	constructor () {
		super();
	}

	render() {
		return (
			<input type="checkbox" name="default" id="default" checked={this.props.checked} onChange={this.props.onChange}></input>
			)
	}
}

class Delete extends React.Component {
	constructor () {
		super();
	}

	render() {
		return (
			<input type="checkbox" name="delete" className="delete"></input>
			)
	}
}

class Submit extends React.Component {
	constructor () {
		super();
	}

	render() {
		return (
			<input type="submit" name="submit_data" onClick={this.props.onClick}></input>
			)
	}
}

// This component holds everything: multiple HotelContainers (which are the hotel dropdown and trash icon) and the addHotel icon
class AllHotelDropDowns extends React.Component {

    constructor() {
    	super();
        this.state = {
            hotels: [],
            defaultView: null,
            compSetIDAndName: [],
            compSetNameDict: {},
            compSetHotels: [],
            hotelContainers: [],
            selectedHotels: [],
            currentSetChoice: null
        };

        this.addHotel = this.addHotel.bind(this);
        this.dropHotelContainer = this.dropHotelContainer.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.changeCompSet = this.changeCompSet.bind(this);
        this.submitData = this.submitData.bind(this);  	// note: you can also use an arrow function in the event handler to avoid having to bind this
		this.changeDefaultBox = this.changeDefaultBox.bind(this);			//  <Submit onClick={() => this.submitData()}/>
    }

    componentDidMount() {
	// AJAX request to get a list of hotels from db
		const hotels = $.get('/sets.json', (data)=> {

			//this returns a list of all hotels that are in the default view
			const defaultHotelsSelected = data['hotels_in_views'][data['default_view']];
			const newHotelContainers = [];
			const newSelectedHotels = [];
			const newCompSetNameDict = {};

			// loop through each hotel that is in the default view, create a hotel container with it, and add it to selected hotels
			for (const hotel of defaultHotelsSelected) {
				newHotelContainers.push({ selectedHotel: hotel });
				newSelectedHotels.push(hotel);
			}

			// create a dictionary of view id and view name
			for (const view of data['view_names']) {
				newCompSetNameDict[view['view_id']] = view['view_name']
			}

			this.setState({ hotels: data['hotels'],
							defaultView: data['default_view'],
							compSetIDAndName: data['view_names'],
							compSetNameDict: newCompSetNameDict,
							compSetHotels: data['hotels_in_views'],
							hotelContainers: newHotelContainers,
							selectedHotels: newSelectedHotels,
							currentSetChoice: data['default_view'],
							checkDefaultBox: true
						})
		})
    }

    handleChange(idx, event) {
    	const newHotelContainers = this.state.hotelContainers.slice();
    	const newSelectedHotels = [];
    	const value = parseInt(event.target.value,10);
    	const selectedValues = document.querySelectorAll('.hotel_dropdown');

    	newHotelContainers[idx] = { selectedHotel: value };
    	newSelectedHotels.push(value);

    	for (const select of selectedValues) {
    		newSelectedHotels.push(parseInt(select.value, 10))
    	}


    	this.setState({ hotelContainers: newHotelContainers,
    					selectedHotels: newSelectedHotels });   	
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

    dropHotelContainer(idx, selectedHotel) {
    	console.log('selected hotel was: ', selectedHotel)

    	const newSelectedHotels = this.state.selectedHotels.slice();

    	// loop through selected hotels and remove the hotel that was just removed
    	newSelectedHotels.map((selection, idx) => {
    		if (selection === selectedHotel) {
    			newSelectedHotels.splice(idx,1)
    		}
    	});

    	// make a copy of newHotelContainers and splice the appropriate hotelContainer
    	const newHotelContainers = this.state.hotelContainers.slice();
		newHotelContainers.splice(idx, 1);
		

    	this.setState({hotelContainers: newHotelContainers,
    					selectedHotels: newSelectedHotels });
    }

    changeCompSet(event) {

    	// update selected hotel
    	const newSetChoice = parseInt(event.target.value,10);
    	const newHotelContainers = [];
    	const newSelectedHotels = [];
    	let checkDefaultValue;

    	// update hotelContainers
    	for (const hotel of this.state.compSetHotels[newSetChoice]) {
			newHotelContainers.push({ selectedHotel: hotel });
			newSelectedHotels.push(hotel);
		}

		if (this.state.defaultView === newSetChoice) {
    		checkDefaultValue = true
    	} else {
    		checkDefaultValue = false
    	}

		this.setState({	currentSetChoice: newSetChoice,
						hotelContainers: newHotelContainers,
						selectedHotels: newSelectedHotels,
						checkDefaultBox: checkDefaultValue 
		})

    }

    changeDefaultBox() {
    	this.setState({ checkDefaultBox: !this.state.checkDefaultBox })
    }

    submitData() {
    	// collect data
    	const deleteSet = document.querySelector('.delete').checked;
    	const compId = this.state.currentSetChoice;
    	const compName = document.querySelector('#set_name').value;
    	const defaultOption = document.querySelector('#default').checked;
    	const hotelsInSet = this.state.selectedHotels;

    	// consolidate all data into one package
    	const data = {	
    					'delete_all' : deleteSet,
    					'set_id' : compId,
    					'set_name' : compName,
    					'default_choice' : defaultOption,
    					'hotels_in_set' : hotelsInSet
    				}

    	$.post('/handle-set-changes', data, (data) => {
    		// this function will display flash messages
    		// clean out the old div where flash messages display

    	})
    }

    render() {

        const hotelContainers = this.state.hotelContainers.map((hotelContainer, idx) => {
            return (
            	<SingleHotelContainer
                	key={idx}
                	handleDropContainer={() => this.dropHotelContainer(idx, hotelContainer.selectedHotel)}
                	handleChange={(event) => this.handleChange(idx, event)} 
                	hotels={this.state.hotels}
                	selectedHotel={hotelContainer.selectedHotel}
                	selectedHotels={this.state.selectedHotels}
                	
            	/>
            );
        });

        return (
            <div className="comp_set_form">
            	<b>Comp Set Selection: </b>
            	<CompSetDropdown 
            		compSetIDAndName={this.state.compSetIDAndName} 
            		currentSetChoice={this.state.currentSetChoice}
            		onChange={this.changeCompSet}
            	/> <br /><br />
            	<b>Comp Set Name: </b> 
            	<CompSetName 
            		currentSetName={this.state.compSetNameDict[this.state.currentSetChoice]}
            	/> <br /> 
            	<b>Default: </b>      
            	<Default 
            		checked={this.state.checkDefaultBox}
            		onChange={this.changeDefaultBox}
            		/><br />	
                <b>Competitors:</b>
                <div className="selected-hotels">
                    {hotelContainers}
                </div>

                <Add onClick={this.addHotel}/>
                <div className="delete_set">
                	<b>DELETE ENTIRE COMP SET  </b>
                	<Delete />
                </div>
                <Submit onClick={this.submitData}/>
           </div> 
        );
	};
}

ReactDOM.render(
	<AllHotelDropDowns />,
	document.getElementById("manage_set")
	);