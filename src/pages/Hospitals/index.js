import axios from 'axios';
import React, {useEffect} from 'react';
import {
  ImageBackground,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import {
  DummyHospital1,
  DummyHospital2,
  DummyHospital3,
  ILHospitalBG,
} from '../../assets';
import {ListHospital} from '../../components';
import {colors, fonts} from '../../utils';

const Hospitals = () => {
  const [data, setData] = React.useState('');

  const geData = async () => {
    try {
      await axios
        .get('https://tugasmd.as.r.appspot.com/getHospital')
        .then(response => {
          setData(response);
        });
    } catch (e) {
      console.log(e);
    }

    const response = await axios.get(
      'https://tugasmd.as.r.appspot.com/getHospital',
    );
    setData(response.data);
  };

  useEffect(() => {
    geData();
  }, []);
  console.log(data);

  var card = [];
  for (let i = 0; i < data.length; i++) {
    const element = data[i];
    card.push(
      <ListHospital
        type="Rumah Sakit"
        name={element.name}
        address={element.address}
        pic={element.image}
        region={element.region}
        phone={element.phone}
      />,
    );
  }

  return (
    <View style={styles.page}>
      <ImageBackground source={ILHospitalBG} style={styles.background}>

      </ImageBackground>
      <ScrollView style={styles.content}>
        <View style={styles.content}>
          {/* <ListHospital
          type="Rumah Sakit"
          name="Citra Bunga Merdeka"
          address="Jln. Surya Sejahtera 20"
          pic={DummyHospital1}
        />
        <ListHospital
          type="Rumah Sakit Anak"
          name="Happy Family & Kids"
          address="Jln. Surya Sejahtera 20"
          pic={DummyHospital2}
        />
        <ListHospital
          type="Rumah Sakit Jiwa"
          name="Tingkatan Paling Atas"
          address="Jln. Surya Sejahtera 20"
          pic={DummyHospital3}
        /> */}
          {card}
        </View>
      </ScrollView>
    </View>
  );
};

export default Hospitals;

const styles = StyleSheet.create({
  background: {
    weight: 360,
    height: 240,
    paddingTop: 30,
  },
  title: {
    fontSize: 20,
    fontFamily: fonts.primary[600],
    color: colors.white,
    textAlign: 'center',
  },
  desc: {
    fontSize: 14,
    fontFamily: fonts.primary[300],
    color: colors.white,
    textAlign: 'center',
    marginTop: 6,
  },
  page: {
    backgroundColor: colors.secondary,
    flex: 1,
  },
  content: {
    backgroundColor: colors.white,
    flex: 1,
    borderRadius: 20,
    marginTop: -30,
    paddingTop: 14,
  },
});
