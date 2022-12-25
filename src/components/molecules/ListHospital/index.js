import {Image, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {DummyHospital1} from '../../../assets';
import {colors} from '../../../utils';

const ListHospital = () => {
  return (
    <View style={styles.container}>
      <Image source={DummyHospital1} style={styles.image} />
      <View>
        <Text style={styles.title}>Rumah Sakit</Text>
        <Text style={styles.title}>Citra Bunga Merdeka</Text>
        <Text style={styles.addres}>Jln. Surya Sejahtera 20</Text>
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
  addres: {
    fontSize: 12,
    color: colors.text.secondary,
    marginTop: 6,
  },
  title: {
    fontSize: 16,
    color: colors.text.primary,
  },
});
