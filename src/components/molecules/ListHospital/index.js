import {Image, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {DummyHospital1} from '../../../assets';
import {colors} from '../../../utils';

const ListHospital = ({type, name, address, pic}) => {
  return (
    <View style={styles.container}>
      <Image source={pic} style={styles.image} />
      <View>
        <Text style={styles.title}>{type}</Text>
        <Text style={styles.title}>{name}</Text>
        <Text style={styles.address}>{address}</Text>
      </View>
    </View>
  );
};

export default ListHospital;

const styles = StyleSheet.create({
  image: {
    width: 80,
    height: 60,
    borderRadius: 11,
    marginRight: 16,
  },
  container: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    padding: 16,
  },
  address: {
    fontSize: 12,
    color: colors.text.secondary,
    marginTop: 6,
  },
  title: {
    fontSize: 16,
    color: colors.text.primary,
  },
});
