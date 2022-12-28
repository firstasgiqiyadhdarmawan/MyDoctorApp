import React, {useState} from 'react';
import {ScrollView, StyleSheet, Text, View} from 'react-native';
import {
  DummyDoctor1,
  DummyDoctor2,
  DummyDoctor3,
  DummyNews1,
  DummyNews2,
  DummyNews3,
  JSONCategoryDoctor,
} from '../../assets';
import {
  DoctorCategory,
  Gap,
  HomeProfile,
  NewsItem,
  RatedDoctor,
} from '../../components';
import {colors, fonts} from '../../utils';

const Doctor = ({navigation}) => {
  const [news] = useState([
    {
      id: 1,
      image: DummyNews1,
      title: 'Is it safe to stay at home during coronavirus?',
      date: 'Today',
    },
    {
      id: 2,
      image: DummyNews2,
      title: 'Consume yellow citrus helps you healthier',
      date: 'Today',
    },
    {
      id: 3,
      image: DummyNews3,
      title: 'Learn how to make a proper orange juice at home',
      date: 'Today',
    },
  ]);
  return (
    <ScrollView showsVerticalScrollIndicator={false}>
      <View style={styles.page}>
        <View style={styles.content}>
          <View style={styles.contentSection}>
            <Gap height={30} />
            <HomeProfile />
            <Gap height={30} />
            <Text style={styles.welcome}>
              Mau konsultasi dengan siapa hari ini?
            </Text>
            <Gap height={16} />
          </View>
          <View style={styles.wrapperScroll}>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <View style={styles.category}>
                <Gap width={32} />
                {JSONCategoryDoctor.data.map(item => {
                  return (
                    <DoctorCategory
                      key={item.id}
                      category={item.category}
                      onPress={() => navigation.navigate('ChooseDoctor')}
                    />
                  );
                })}
                <Gap width={22} />
              </View>
            </ScrollView>
          </View>
          <View style={styles.contentSection}>
            <Text style={styles.sectionLabel}>Top Rated Doctors</Text>
            <RatedDoctor
              profile={DummyDoctor1}
              name="Alexa Rachel"
              category="Pediatrician"
            />
            <RatedDoctor
              profile={DummyDoctor2}
              name="Sunny Frank"
              category="Dentist"
            />
            <RatedDoctor
              profile={DummyDoctor3}
              name="Poe Minn"
              category="Podiatrist"
            />
            <Text style={styles.sectionLabel2}>Good News</Text>
            {news.map(news => {
              return (
                <NewsItem
                  key={news.id}
                  image={news.image}
                  title={news.title}
                  date={news.date}
                />
              );
            })}
            {/* <NewsItem />
            <NewsItem />
            <NewsItem /> */}
            <Gap height={30} />
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

export default Doctor;

const styles = StyleSheet.create({
  contentSection: {
    paddingHorizontal: 16,
  },
  page: {
    backgroundColor: colors.secondary,
    flex: 1,
  },
  welcome: {
    fontSize: 20,
    fontFamily: fonts.primary[600],
    color: colors.text.primary,
    maxWidth: 211,
  },
  category: {
    flexDirection: 'row',
  },
  wrapperScroll: {
    marginHorizontal: -16,
  },
  content: {
    backgroundColor: colors.white,
    flex: 1,
    // paddingVertical: 30,
    // paddingHorizontal: 16,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  sectionLabel: {
    fontSize: 16,
    fontFamily: fonts.primary[600],
    color: colors.text.primary,
    marginTop: 30,
    marginBottom: 16,
  },
  sectionLabel2: {
    fontSize: 16,
    fontFamily: fonts.primary[600],
    color: colors.text.primary,
    marginTop: 14,
    marginBottom: 16,
  },
});
