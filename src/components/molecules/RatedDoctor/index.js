import React from 'react';
import {Image, StyleSheet, Text, View} from 'react-native';
import {IconStar} from '../../../assets';
import {colors, fonts} from '../../../utils';

const RatedDoctor = ({profile, name, category}) => {
  return (
    <View style={styles.container}>
      <Image source={profile} style={styles.avatar} />
      <View style={styles.profile}>
        <Text style={styles.name}>{name}</Text>
        <Text style={styles.category}>{category}</Text>
      </View>

      <View style={styles.rate}>
        <IconStar />
        <IconStar />
        <IconStar />
        <IconStar />
        <IconStar />
      </View>
    </View>
  );
};

export default RatedDoctor;

const styles = StyleSheet.create({
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 50 / 2,
    marginRight: 12,
  },
  container: {
    // justifyContent: 'space-evenly',
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingBottom: 16,
    // paddingHorizontal: 16,
  },
  rate: {
    flexDirection: 'row',
    marginLeft: 67,
    alignItems: 'center',
  },
  name: {
    fontSize: 16,
    fontFamily: fonts.primary[600],
    color: colors.text.primary,
  },
  category: {
    fontFamily: fonts.primary.normal,
    fontSize: 12,
    color: colors.text.secondary,
  },
  profile: {
    flex: 1,
  },
});
